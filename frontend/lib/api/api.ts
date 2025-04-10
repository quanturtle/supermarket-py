const API_CONFIG = {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
}


// apiRequest ------------------------------------------------------
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

// getAllProducts ------------------------------------------------------
export type ProductListResult = {
    id: number
    name: string
    sku: string
}

export async function getAllProducts(): Promise<ProductListResult[]> {
    return apiRequest<ProductListResult[]>("/products")
}


// getProductBySKU ------------------------------------------------------
export type ProductHistoryEntry = {
    supermarket_id: number;
    name: string;
    price: number;
    created_at: string;
};

export type ProductInfo = {
    name: string;
    sku: string;
};

export type PriceChange = {
    supermarket_id: number;
    price: number;
    pct_change: number;
};

export type ProductDetailResult = {
    history: ProductHistoryEntry[];
    product_info: ProductInfo;
    price_changes: PriceChange[];
};

export async function getProductBySKU(sku: string): Promise<ProductDetailResult> {
    return apiRequest<ProductDetailResult>(`/products/${sku}`)
}


// searchProducts ------------------------------------------------------
export async function searchProducts(name: string): Promise<ProductListResult[]> {
    return apiRequest<ProductListResult[]>(`/products/search/?query=${encodeURIComponent(name)}`)
}


// getPriceComparison ------------------------------------------------------
export type ShoppingListItem = {
    sku: string;
    quantity: number;
};

export type ProductFull = {
    supermarket_id: number;
    name: string;
    sku: string;
    price: number;
    created_at: string;
};

export type PriceComparisonResult = {
    optimal: ProductFull[];
    best: ProductFull[];
    median: ProductFull[];
    worst: ProductFull[];
};

export async function getPriceComparison(shoppingList: ShoppingListItem[]): Promise<PriceComparisonResult> {
    return apiRequest<PriceComparisonResult>("/price-comparison", {
        method: "POST",
        body: JSON.stringify(shoppingList),
    });
}


// calculateInflation ------------------------------------------------------
export type InflationRequestBody = {
    shopping_list: ShoppingListItem[];
    date_range: [string, string];
};

export type InflationResult = {
    mean: number;
    min: number;
    gap: number;
};

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


// configureApi ------------------------------------------------------
export function configureApi(config: { baseUrl?: string }) {
    if (config.baseUrl) {
        API_CONFIG.baseUrl = config.baseUrl
    }
}


// ------------------------------------------------------
export const API = {
    getAllProducts,
    getProductBySKU,
    searchProducts,
    getPriceComparison,
    calculateInflation,
    configure: configureApi,
}