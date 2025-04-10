"use client"

import { useState, useEffect, useCallback } from "react"
import { API, type InflationResult, type ProductListResult, type DateRangeResult } from "@/lib/api/api"
import { toast } from "@/hooks/use-toast"

// Import our modular components
import { ProductSelection } from "@/components/inflation/product-selection"
import { DateSelection } from "@/components/inflation/date-selection"
import { InflationResults } from "@/components/inflation/inflation-results"

export default function InflationCalculatorPage() {
  const [products, setProducts] = useState<ProductListResult[]>([])
  const [loading, setLoading] = useState(true)
  const [calculating, setCalculating] = useState(false)
  const [selectedProducts, setSelectedProducts] = useState<string[]>([])

  // Date range state
  const [dateRange, setDateRange] = useState<DateRangeResult | null>(null)
  const [startDate, setStartDate] = useState<string>("")
  const [endDate, setEndDate] = useState<string>("")
  const [availableDates, setAvailableDates] = useState<string[]>([])

  const [inflationResults, setInflationResults] = useState<InflationResult | null>(null)

  // Load products and date range on component mount
  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true)

        // Load products and date range in parallel
        const [productsData, dateRangeData] = await Promise.all([API.getAllProducts(), API.getInflationDateRange()])

        setProducts(productsData)
        setDateRange(dateRangeData)

        // Generate available dates between start_date and end_date
        if (dateRangeData) {
          const start = new Date(dateRangeData.start_date)
          const end = new Date(dateRangeData.end_date)
          const dates: string[] = []

          const currentDate = new Date(start)
          while (currentDate <= end) {
            dates.push(currentDate.toISOString().split("T")[0])
            currentDate.setDate(currentDate.getDate() + 1)
          }

          setAvailableDates(dates)
          setStartDate(dateRangeData.start_date)
          setEndDate(dateRangeData.end_date)
        }
      } catch (error) {
        console.error("Error loading initial data:", error)
        toast({
          title: "Error loading data",
          description: "Could not load product data or date range. Please try again later.",
          variant: "destructive",
        })
      } finally {
        setLoading(false)
      }
    }

    loadInitialData()
  }, [])

  // Handle product selection toggle
  const handleProductToggle = useCallback((productSku: string) => {
    setSelectedProducts((prev) =>
      prev.includes(productSku) ? prev.filter((sku) => sku !== productSku) : [...prev, productSku],
    )
  }, [])

  // Function to handle inflation calculation
  const handleCalculate = useCallback(async () => {
    if (selectedProducts.length === 0) {
      toast({
        title: "No products selected",
        description: "Please select at least one product to calculate inflation.",
        variant: "destructive",
      })
      return
    }

    setCalculating(true)
    try {
      // Create the shopping list from selected products
      const shoppingList = selectedProducts.map((sku) => ({
        sku,
        quantity: 1,
      }))

      // Call the API with the dates directly
      const results = await API.calculateInflation(shoppingList, [startDate, endDate])
      setInflationResults(results)
    } catch (error) {
      console.error("Error calculating inflation:", error)
      toast({
        title: "Calculation error",
        description: "An error occurred while calculating inflation. Please try again.",
        variant: "destructive",
      })
    } finally {
      setCalculating(false)
    }
  }, [selectedProducts, startDate, endDate])

  if (loading) {
    return (
      <div className="container flex items-center justify-center min-h-screen">
        <p>Loading products and date range...</p>
      </div>
    )
  }

  // Format the results for the InflationResults component
  const formattedResults = inflationResults
    ? {
        averagePriceInflation: {
          startPrice: inflationResults.global_inflation.mean_inflation.start_price.toFixed(2),
          endPrice: inflationResults.global_inflation.mean_inflation.end_price.toFixed(2),
          absoluteChange: inflationResults.global_inflation.mean_inflation.absolute_change.toFixed(2),
          percentageChange: inflationResults.global_inflation.mean_inflation.inflation_rate.toFixed(2),
        },
        lowestPriceInflation: {
          startPrice: inflationResults.global_inflation.min_inflation.start_price.toFixed(2),
          endPrice: inflationResults.global_inflation.min_inflation.end_price.toFixed(2),
          absoluteChange: inflationResults.global_inflation.min_inflation.absolute_change.toFixed(2),
          percentageChange: inflationResults.global_inflation.min_inflation.inflation_rate.toFixed(2),
        },
        priceGapInflation: {
          startGap: inflationResults.global_inflation.gap_inflation.start_price.toFixed(2),
          endGap: inflationResults.global_inflation.gap_inflation.end_price.toFixed(2),
          absoluteChange: inflationResults.global_inflation.gap_inflation.absolute_change.toFixed(2),
          percentageChange: inflationResults.global_inflation.gap_inflation.inflation_rate.toFixed(2),
        },
        productInflation: inflationResults.per_product_inflation,
        startDate,
        endDate,
      }
    : null

  return (
    <>
      <h1 className="text-3xl font-bold mb-6">Inflation Calculator</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:gap-8">
        {/* Product Selection */}
        <ProductSelection
          products={products}
          selectedProducts={selectedProducts}
          onToggleProduct={handleProductToggle}
        />

        {/* Date Selection and Calculation */}
        <DateSelection
          availableDates={availableDates}
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
          onCalculate={handleCalculate}
          isCalculateDisabled={selectedProducts.length === 0 || calculating}
        />
      </div>

      {/* Loading State */}
      {calculating && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-sm animate-pulse">
          <div className="h-8 bg-gray-200 rounded mb-4 w-1/3"></div>
          <div className="grid gap-6 md:grid-cols-3">
            <div className="h-40 bg-gray-200 rounded"></div>
            <div className="h-40 bg-gray-200 rounded"></div>
            <div className="h-40 bg-gray-200 rounded"></div>
          </div>
          <div className="h-60 bg-gray-200 rounded mt-6"></div>
        </div>
      )}

      {/* Results Section */}
      {!calculating && formattedResults && <InflationResults results={formattedResults} />}
    </>
  )
}
