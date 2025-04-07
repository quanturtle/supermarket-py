import { mockProducts, type ProductData } from "@/lib/data/product-data"

// Simulate network delay
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

/**
 * API class to simulate backend calls
 */
export class API {
    /**
     * Get all products
     */
    static async getProducts(): Promise<ProductData[]> {
        await delay(500) // Simulate network delay
        return Object.values(mockProducts).sort((a, b) => a.name.localeCompare(b.name))
    }

    /**
     * Get a product by ID
     */
    static async getProductById(id: string): Promise<ProductData | null> {
        await delay(300) // Simulate network delay
        const product = Object.values(mockProducts).find((product) => product.id === id)
        return product || null
    }

    /**
     * Get a product by slug (name)
     */
    static async getProductBySlug(slug: string): Promise<ProductData | null> {
        await delay(300) // Simulate network delay
        const product = Object.values(mockProducts).find(
            (product) => product.name.toLowerCase().replace(/[^a-z0-9]+/g, "-") === slug,
        )
        return product || null
    }

    /**
     * Search products by query
     */
    static async searchProducts(query: string): Promise<ProductData[]> {
        await delay(400) // Simulate network delay
        if (!query.trim()) return []

        const lowercaseQuery = query.toLowerCase()
        return Object.values(mockProducts).filter(
            (product) =>
                product.name.toLowerCase().includes(lowercaseQuery) ||
                product.description.toLowerCase().includes(lowercaseQuery) ||
                product.sku.toLowerCase().includes(lowercaseQuery),
        )
    }

    /**
     * Add item to cart (simulated)
     */
    static async addToCart(productId: string, quantity: number): Promise<{ success: boolean }> {
        await delay(200) // Simulate network delay
        // In a real app, this would make a POST request to add the item to the cart
        return { success: true }
    }

    /**
     * Get price comparison for selected products
     */
    static async getPriceComparison(productIds: string[], quantities: Record<string, number>): Promise<any> {
        await delay(700) // Simulate network delay

        // Get products by IDs
        const products = productIds.map(
            (id) =>
                mockProducts[
                Object.keys(mockProducts).find(
                    (key) => mockProducts[key as keyof typeof mockProducts].id === id,
                ) as keyof typeof mockProducts
                ],
        )

        // Get all supermarket names from the first product
        if (!products.length) return null
        const supermarketsList = Object.keys(products[0].currentPrices)

        // Calculate total price for each supermarket
        const supermarketPricing = supermarketsList.map((supermarket) => {
            let totalPrice = 0
            const items = products.map((product) => {
                const price = product.currentPrices[supermarket]
                const quantity = quantities[product.id] || 1
                const total = price * quantity
                totalPrice += total

                return {
                    productId: product.id,
                    price,
                    total,
                }
            })

            return {
                name: supermarket,
                totalPrice,
                items,
            }
        })

        // Sort by total price
        supermarketPricing.sort((a, b) => a.totalPrice - b.totalPrice)

        // Find worst, average, and best supermarkets
        const worst = supermarketPricing[supermarketPricing.length - 1]
        const average = supermarketPricing[Math.floor(supermarketPricing.length / 2)]
        const best = supermarketPricing[0]

        // Calculate optimal combination
        let optimalTotalPrice = 0
        const optimalItems = products.map((product) => {
            // Find the supermarket with the lowest price for this product
            const supermarketPrices = Object.entries(product.currentPrices)
            supermarketPrices.sort((a, b) => a[1] - b[1])

            const [bestSupermarket, lowestPrice] = supermarketPrices[0]
            const quantity = quantities[product.id] || 1
            const total = lowestPrice * quantity
            optimalTotalPrice += total

            return {
                productId: product.id,
                supermarket: bestSupermarket,
                price: lowestPrice,
                total,
            }
        })

        return {
            worst,
            average,
            best,
            optimal: {
                totalPrice: optimalTotalPrice,
                items: optimalItems,
            },
        }
    }

    /**
     * Calculate inflation between two time periods
     */
    static async calculateInflation(productIds: string[], startDate: string, endDate: string): Promise<any> {
        await delay(800) // Simulate network delay

        // Get products by IDs
        const selectedProducts = productIds.map(
            (id) =>
                mockProducts[
                Object.keys(mockProducts).find(
                    (key) => mockProducts[key as keyof typeof mockProducts].id === id,
                ) as keyof typeof mockProducts
                ],
        )

        // Calculate average price inflation
        let startTotalPrice = 0
        let endTotalPrice = 0

        selectedProducts.forEach((product) => {
            const startPriceData = product.priceHistory.find((history) => history.date === startDate)
            const endPriceData = product.priceHistory.find((history) => history.date === endDate)

            if (startPriceData && endPriceData) {
                // Calculate average price for each time period
                const startSupermarketPrices = Object.entries(startPriceData)
                    .filter(([key]) => key !== "date")
                    .map(([, value]) => Number(value))

                const endSupermarketPrices = Object.entries(endPriceData)
                    .filter(([key]) => key !== "date")
                    .map(([, value]) => Number(value))

                const startAvgPrice =
                    startSupermarketPrices.reduce((sum, price) => sum + price, 0) / startSupermarketPrices.length
                const endAvgPrice = endSupermarketPrices.reduce((sum, price) => sum + price, 0) / endSupermarketPrices.length

                startTotalPrice += startAvgPrice
                endTotalPrice += endAvgPrice
            }
        })

        const avgPercentageChange = ((endTotalPrice - startTotalPrice) / startTotalPrice) * 100

        // Calculate lowest price inflation
        let startTotalLowestPrice = 0
        let endTotalLowestPrice = 0

        selectedProducts.forEach((product) => {
            const startPriceData = product.priceHistory.find((history) => history.date === startDate)
            const endPriceData = product.priceHistory.find((history) => history.date === endDate)

            if (startPriceData && endPriceData) {
                // Find lowest price for each time period
                const startSupermarketPrices = Object.entries(startPriceData)
                    .filter(([key]) => key !== "date")
                    .map(([, value]) => Number(value))

                const endSupermarketPrices = Object.entries(endPriceData)
                    .filter(([key]) => key !== "date")
                    .map(([, value]) => Number(value))

                const startLowestPrice = Math.min(...startSupermarketPrices)
                const endLowestPrice = Math.min(...endSupermarketPrices)

                startTotalLowestPrice += startLowestPrice
                endTotalLowestPrice += endLowestPrice
            }
        })

        const lowestPercentageChange = ((endTotalLowestPrice - startTotalLowestPrice) / startTotalLowestPrice) * 100

        // Calculate price gap inflation
        const productGapChanges = selectedProducts
            .map((product) => {
                const startPriceData = product.priceHistory.find((history) => history.date === startDate)
                const endPriceData = product.priceHistory.find((history) => history.date === endDate)

                if (startPriceData && endPriceData) {
                    // Calculate price gap for each time period
                    const startSupermarketPrices = Object.entries(startPriceData)
                        .filter(([key]) => key !== "date")
                        .map(([, value]) => Number(value))

                    const endSupermarketPrices = Object.entries(endPriceData)
                        .filter(([key]) => key !== "date")
                        .map(([, value]) => Number(value))

                    const startLowestPrice = Math.min(...startSupermarketPrices)
                    const startHighestPrice = Math.max(...startSupermarketPrices)
                    const startGap = startHighestPrice - startLowestPrice

                    const endLowestPrice = Math.min(...endSupermarketPrices)
                    const endHighestPrice = Math.max(...endSupermarketPrices)
                    const endGap = endHighestPrice - endLowestPrice

                    return {
                        name: product.name,
                        startGap,
                        endGap,
                        absoluteChange: endGap - startGap,
                        percentageChange: startGap === 0 ? 0 : ((endGap - startGap) / startGap) * 100,
                    }
                }
                return null
            })
            .filter(Boolean)

        // Calculate average start gap and end gap
        const totalStartGap = productGapChanges.reduce((sum, item) => sum + item!.startGap, 0)
        const totalEndGap = productGapChanges.reduce((sum, item) => sum + item!.endGap, 0)
        const avgStartGap = totalStartGap / productGapChanges.length
        const avgEndGap = totalEndGap / productGapChanges.length

        // Calculate average percentage change
        const gapPercentageChange =
            productGapChanges.reduce((sum, item) => sum + item!.percentageChange, 0) / productGapChanges.length

        // Calculate per-product inflation
        const productInflation = selectedProducts
            .map((product) => {
                const startPriceData = product.priceHistory.find((history) => history.date === startDate)
                const endPriceData = product.priceHistory.find((history) => history.date === endDate)

                if (startPriceData && endPriceData) {
                    // Calculate average price for each time period
                    const startSupermarketPrices = Object.entries(startPriceData)
                        .filter(([key]) => key !== "date")
                        .map(([, value]) => Number(value))

                    const endSupermarketPrices = Object.entries(endPriceData)
                        .filter(([key]) => key !== "date")
                        .map(([, value]) => Number(value))

                    const startAvgPrice =
                        startSupermarketPrices.reduce((sum, price) => sum + price, 0) / startSupermarketPrices.length
                    const endAvgPrice = endSupermarketPrices.reduce((sum, price) => sum + price, 0) / endSupermarketPrices.length

                    const percentageChange = ((endAvgPrice - startAvgPrice) / startAvgPrice) * 100

                    return {
                        id: product.id,
                        name: product.name,
                        startPrice: startAvgPrice.toFixed(2),
                        endPrice: endAvgPrice.toFixed(2),
                        absoluteChange: (endAvgPrice - startAvgPrice).toFixed(2),
                        percentageChange: percentageChange.toFixed(2),
                    }
                }
                return null
            })
            .filter(Boolean)
            .sort((a, b) => Number(b.percentageChange) - Number(a.percentageChange))

        return {
            averagePriceInflation: {
                startPrice: startTotalPrice.toFixed(2),
                endPrice: endTotalPrice.toFixed(2),
                absoluteChange: (endTotalPrice - startTotalPrice).toFixed(2),
                percentageChange: avgPercentageChange.toFixed(2),
            },
            lowestPriceInflation: {
                startPrice: startTotalLowestPrice.toFixed(2),
                endPrice: endTotalLowestPrice.toFixed(2),
                absoluteChange: (endTotalLowestPrice - startTotalLowestPrice).toFixed(2),
                percentageChange: lowestPercentageChange.toFixed(2),
            },
            priceGapInflation: {
                startGap: avgStartGap.toFixed(2),
                endGap: avgEndGap.toFixed(2),
                absoluteChange: (avgEndGap - avgStartGap).toFixed(2),
                percentageChange: gapPercentageChange.toFixed(2),
            },
            productInflation,
            startDate,
            endDate,
        }
    }
}