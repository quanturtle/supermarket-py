const API_CONFIG = {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
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


export type Product = {
    id: number
    name: string
    supermarket_id: number
    sku: string
    price: number
    created_at: string
}

export type ProductList = {
    id: number
    name: string
    sku: string
}

export async function getAllProducts(): Promise<ProductList[]> {
    return apiRequest<Product[]>("/products")
}

export async function getProductById(id: number): Promise<Product> {
    return apiRequest<Product>(`/products/${id}`)
}

export async function searchProducts(query: string): Promise<Product[]> {
    return apiRequest<Product[]>(`/products/search/?query=${encodeURIComponent(query)}`)
}

export type ShoppingListItem = {
    sku: string
}

export type PriceComparisonResult = {
    optimal: Product[]
    best: Product[]
    median: Product[]
    worst: Product[]
}

export async function getPriceComparison(
    shoppingList: ShoppingListItem[]
): Promise<PriceComparisonResult> {
    return apiRequest<PriceComparisonResult>("/price-comparison", {
        method: "POST",
        body: JSON.stringify(shoppingList),
    })
}

export type InflationResult = {
    mean: number
    min: number
    gap: number
}

export async function calculateInflation(
    shoppingList: ShoppingListItem[],
    dateRange: [string, string]
): Promise<InflationResult> {
    return apiRequest<InflationResult>("/inflation", {
        method: "POST",
        body: JSON.stringify({
            shopping_list: shoppingList,
            date_range: dateRange
        }),
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
    getPriceComparison,
    calculateInflation,
    configure: configureApi,
}