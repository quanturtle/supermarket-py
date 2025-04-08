const API_CONFIG = {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
}

export type ProductData = {
    id: string
    name: string
    image: string
    sku: string
    description: string
    currentPrices: {
        [key: string]: number
    }
    priceChanges: {
        [key: string]: number
    }
    lowestPrice: {
        price: number
        store: string
    }
    priceHistory: Array<{
        date: string
        [key: string]: string | number
    }>
}

async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_CONFIG.baseUrl}${endpoint}`
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
        })
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status} ${response.statusText}`)
        }
        return (await response.json()) as T
    } catch (error) {
        console.error("API request error:", error)
        throw error
    }
}

export async function getAllProducts(): Promise<ProductData[]> {
    return apiRequest<ProductData[]>("/api/products")
}

export async function getProductById(id: string): Promise<ProductData | null> {
    return apiRequest<ProductData | null>(`/api/products/${id}`)
}

export async function searchProducts(query: string): Promise<ProductData[]> {
    return apiRequest<ProductData[]>(`/api/products/search?q=${encodeURIComponent(query)}`)
}

export async function addToCart(productId: string, quantity: number): Promise<{ success: boolean }> {
    return apiRequest<{ success: boolean }>("/api/cart/add", {
        method: "POST",
        body: JSON.stringify({ productId, quantity }),
    })
}

export async function getPriceComparison(
    productIds: string[],
    quantities: Record<string, number>,
): Promise<{
    worst: any
    average: any
    best: any
    optimal: {
        totalPrice: number
        items: any[]
    }
}> {
    return apiRequest("/api/price-comparison", {
        method: "POST",
        body: JSON.stringify({ productIds, quantities }),
    })
}

export async function calculateInflation(
    productIds: string[],
    startDate: string,
    endDate: string,
): Promise<{
    averagePriceInflation: any
    lowestPriceInflation: any
    priceGapInflation: any
    productInflation: any[]
    startDate: string
    endDate: string
}> {
    return apiRequest("/api/inflation", {
        method: "POST",
        body: JSON.stringify({ productIds, startDate, endDate }),
    })
}

export function configureApi(config: { baseUrl?: string }) {
    if (config.baseUrl) {
        API_CONFIG.baseUrl = config.baseUrl
    }
}

export const API = {
    getAllProducts,
    getProductById,
    searchProducts,
    addToCart,
    getPriceComparison,
    calculateInflation,
    configure: configureApi,
}  