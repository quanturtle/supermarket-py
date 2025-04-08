"use client"

import { useState, useEffect } from "react"
import type { ProductData } from "@/lib/data/product-data"
import { API } from "@/lib/api/api"
// import { CenteredContent } from "@/components/layout/centered-content"

// Import our modular components
import { ProductSelectionCard } from "@/components/inflation/product-selection-card"
import { DateSelectionCard } from "@/components/inflation/date-selection-card"
import { InflationResultsSection } from "@/components/inflation/inflation-results-section"

export default function InflationCalculatorPage() {
    const [products, setProducts] = useState<ProductData[]>([])
    const [loading, setLoading] = useState(true)
    const [calculating, setCalculating] = useState(false)
    const [selectedProducts, setSelectedProducts] = useState<string[]>([])
    const [startDate, setStartDate] = useState("Jan 2024")
    const [endDate, setEndDate] = useState("Apr 2024")
    const [calculationResults, setCalculationResults] = useState<any>(null)

    // Available time periods from our data
    const availableDates = ["Jan 2024", "Feb 2024", "Mar 2024", "Apr 2024"]

    useEffect(() => {
        async function loadProducts() {
            try {
                const allProducts = await API.getAllProducts()
                setProducts(allProducts)
            } catch (error) {
                console.error("Error loading products:", error)
            } finally {
                setLoading(false)
            }
        }

        loadProducts()
    }, [])

    const handleProductToggle = (productId: string) => {
        setSelectedProducts((prev) =>
            prev.includes(productId) ? prev.filter((id) => id !== productId) : [...prev, productId],
        )
    }

    // Add this function to validate date selection
    const validateDateSelection = () => {
        if (selectedProducts.length === 0) {
            alert("Please select at least one product")
            return false
        }

        return true
    }

    const calculateInflation = async () => {
        if (!validateDateSelection()) return

        setCalculating(true)
        try {
            const results = await API.calculateInflation(selectedProducts, startDate, endDate)

            setCalculationResults(results)
        } catch (error) {
            console.error("Error calculating inflation:", error)
            alert("An error occurred while calculating inflation")
        } finally {
            setCalculating(false)
        }
    }

    if (loading) {
        return (
            <div className="container flex items-center justify-center min-h-screen">
                <p>Loading products...</p>
            </div>
        )
    }

    return (
        <>
            <h1 className="text-3xl font-bold mb-6">Inflation Calculator</h1>

            <div className="grid gap-6 md:grid-cols-2 lg:gap-8">
                {/* Product Selection */}
                <ProductSelectionCard
                    products={products}
                    selectedProducts={selectedProducts}
                    onToggleProduct={handleProductToggle}
                />

                {/* Date Selection and Calculation */}
                <DateSelectionCard
                    availableDates={availableDates}
                    startDate={startDate}
                    endDate={endDate}
                    onStartDateChange={setStartDate}
                    onEndDateChange={setEndDate}
                    onCalculate={calculateInflation}
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
            {!calculating && calculationResults && <InflationResultsSection results={calculationResults} />}
        </>
    )
}