"use client"

import { useState, useEffect, useCallback } from "react"
import { API, type InflationResult, type ProductListResult } from "@/lib/api/api"
import { toast } from "@/hooks/use-toast"

// Import our modular components
import { ProductSelection } from "@/components/inflation/product-selection"
import { DateSelection } from "@/components/inflation/date-selection"
import { InflationResults } from "@/components/inflation/inflation-results"

// Function to get available dates in yyyy-mm-dd format
function getAvailableDates(): string[] {
  return ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01"]
}

export default function InflationCalculatorPage() {
  const [products, setProducts] = useState<ProductListResult[]>([])
  const [loading, setLoading] = useState(true)
  const [calculating, setCalculating] = useState(false)
  const [selectedProducts, setSelectedProducts] = useState<string[]>([])

  // Get available dates and set initial values
  const availableDates = getAvailableDates()
  const [startDate, setStartDate] = useState(availableDates[0])
  const [endDate, setEndDate] = useState(availableDates[availableDates.length - 1])

  const [inflationResults, setInflationResults] = useState<InflationResult | null>(null)

  // Load products on component mount
  useEffect(() => {
    async function loadProducts() {
      try {
        setLoading(true)
        const allProducts = await API.getAllProducts()
        setProducts(allProducts)
      } catch (error) {
        console.error("Error loading products:", error)
        toast({
          title: "Error loading products",
          description: "Could not load product data. Please try again later.",
          variant: "destructive",
        })
      } finally {
        setLoading(false)
      }
    }

    loadProducts()
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
        <p>Loading products...</p>
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
