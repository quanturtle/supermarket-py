// Type definitions
export type ProductListResult = {
  id: number
  name: string
  sku: string
}

export type ProductHistoryEntry = {
  supermarket_id: number
  name: string
  price: number
  created_at: string
}

export type ProductInfo = {
  name: string
  sku: string
}

export type PriceChange = {
  supermarket_id: number
  price: number
  pct_change: number
}

export type ProductDetailResult = {
  history: ProductHistoryEntry[]
  product_info: ProductInfo
  price_changes: PriceChange[]
}

export type ShoppingListItem = {
  sku: string
  quantity: number
}

export type ProductFull = {
  supermarket_id: number
  name: string
  sku: string
  price: number
  created_at: string
}

export type PriceComparisonResult = {
  optimal: ProductFull[]
  best: ProductFull[]
  median: ProductFull[]
  worst: ProductFull[]
}

export type InflationRequestBody = {
  shopping_list: ShoppingListItem[]
  date_range: [string, string]
}

// Type definitions for inflation
export type InflationMetric = {
  start_price: number
  end_price: number
  absolute_change: number
  inflation_rate: number
}

export type GlobalInflation = {
  mean_inflation: InflationMetric
  min_inflation: InflationMetric
  gap_inflation: InflationMetric
}

export type ProductInflation = {
  sku: string
  name: string
  inflation_rate: number
}

export type InflationResult = {
  global_inflation: GlobalInflation
  per_product_inflation: ProductInflation[]
}

// Import mock data
import { MOCK_PRODUCTS, MOCK_PRODUCT_DETAILS, MOCK_PRICE_COMPARISON, MOCK_INFLATION } from "@/lib/data/example-data"

// API Configuration
const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
}

/**
 * Handles API errors and returns fallback data
 * @param error The error that occurred
 * @param fallbackData The fallback data to return
 * @param errorMessage Custom error message
 */
function handleApiError<T>(error: unknown, fallbackData: T, errorMessage: string): T {
  console.error(`ERROR: ${errorMessage}`, error)
  return fallbackData
}

/**
 * Makes an API request with error handling
 * @param url The URL to fetch
 * @param options Fetch options
 * @param fallbackData Fallback data if the request fails
 */
async function apiRequest<T>(url: string, options?: RequestInit, fallbackData?: T): Promise<T> {
  try {
    const response = await fetch(url, options)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    if (!fallbackData) {
      throw error
    }
    return handleApiError(error, fallbackData, `Failed to fetch from ${url}`)
  }
}

// API Functions

// Get all products
export async function getAllProducts(): Promise<ProductListResult[]> {
  return apiRequest(`${API_CONFIG.baseUrl}/products/`, undefined, MOCK_PRODUCTS)
}

// Get product by SKU
export async function getProductBySKU(sku: string): Promise<ProductDetailResult> {
  const fallbackData = MOCK_PRODUCT_DETAILS[sku] || {
    history: [],
    product_info: { name: "Unknown Product", sku },
    price_changes: [],
  }

  return apiRequest(`${API_CONFIG.baseUrl}/product/${sku}`, undefined, fallbackData)
}

// Search products by name
export async function searchProducts(query: string): Promise<ProductListResult[]> {
  // Filter mock products for fallback based on query
  const mockSearchResults = MOCK_PRODUCTS.filter((product) =>
    product.name.toLowerCase().includes(query.toLowerCase()),
  ).slice(0, 5)

  return apiRequest(
    `${API_CONFIG.baseUrl}/products/search/?query=${encodeURIComponent(query)}`,
    undefined,
    mockSearchResults,
  )
}

// Get price comparison
export async function getPriceComparison(shoppingList: ShoppingListItem[]): Promise<PriceComparisonResult> {
  return apiRequest(
    `${API_CONFIG.baseUrl}/price-comparison`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(shoppingList),
    },
    MOCK_PRICE_COMPARISON,
  )
}

// Calculate inflation
export async function calculateInflation(
  shoppingList: ShoppingListItem[],
  dateRange: [string, string],
): Promise<InflationResult> {
  return apiRequest(
    `${API_CONFIG.baseUrl}/inflation`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        shopping_list: shoppingList,
        date_range: dateRange,
      }),
    },
    MOCK_INFLATION,
  )
}

// Configure API
export function configureApi(config: { baseUrl?: string }): void {
  if (config.baseUrl) {
    API_CONFIG.baseUrl = config.baseUrl
  }
}

// Export all functions
export const API = {
  getAllProducts,
  getProductBySKU,
  searchProducts,
  getPriceComparison,
  calculateInflation,
  configure: configureApi,

  // Alias for backward compatibility
  getProducts: getAllProducts,
}
