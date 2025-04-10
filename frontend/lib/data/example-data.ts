// Mock products for fallback - reduced to only include products with detailed information
export const MOCK_PRODUCTS: ProductListResult[] = [
  {
    id: 97,
    name: "White Bread (500g)",
    sku: "BREAD-WHT-500G",
  },
  {
    id: 180,
    name: "Eggs (Dozen)",
    sku: "EGGS-LRG-12CT",
  },
  {
    id: 37,
    name: "Whole Milk (1 Liter)",
    sku: "MILK-1L-WHL",
  },
  {
    id: 42,
    name: "Bananas (1kg)",
    sku: "FRUIT-BAN-1KG",
  },
  {
    id: 1,
    name: "Whole Milk (1 Gallon)",
    sku: "MILK-1GAL-WHL",
  },
]

// Mock product detail for fallback
export const MOCK_PRODUCT_DETAILS: Record<string, ProductDetailResult> = {
  "BREAD-WHT-500G": {
    history: [
      {
        supermarket_id: 1,
        name: "White Bread (500g)",
        price: 1.49,
        created_at: "2025-01-01 08:05:00",
      },
      {
        supermarket_id: 1,
        name: "White Bread (500g)",
        price: 1.59,
        created_at: "2025-02-01 08:05:00",
      },
      {
        supermarket_id: 1,
        name: "White Bread (500g)",
        price: 1.69,
        created_at: "2025-03-01 08:05:00",
      },
      {
        supermarket_id: 1,
        name: "White Bread (500g)",
        price: 1.79,
        created_at: "2025-04-01 08:05:00",
      },
      {
        supermarket_id: 2,
        name: "White Bread (500g)",
        price: 1.39,
        created_at: "2025-01-01 09:15:00",
      },
      {
        supermarket_id: 2,
        name: "White Bread (500g)",
        price: 1.49,
        created_at: "2025-02-01 09:15:00",
      },
      {
        supermarket_id: 2,
        name: "White Bread (500g)",
        price: 1.59,
        created_at: "2025-03-01 09:15:00",
      },
      {
        supermarket_id: 2,
        name: "White Bread (500g)",
        price: 1.69,
        created_at: "2025-04-01 09:15:00",
      },
      {
        supermarket_id: 3,
        name: "White Bread (500g)",
        price: 1.59,
        created_at: "2025-01-01 10:25:00",
      },
      {
        supermarket_id: 3,
        name: "White Bread (500g)",
        price: 1.69,
        created_at: "2025-02-01 10:25:00",
      },
      {
        supermarket_id: 3,
        name: "White Bread (500g)",
        price: 1.79,
        created_at: "2025-03-01 10:25:00",
      },
      {
        supermarket_id: 3,
        name: "White Bread (500g)",
        price: 1.89,
        created_at: "2025-04-01 10:25:00",
      },
    ],
    product_info: {
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 1.79,
        pct_change: 0.06,
      },
      {
        supermarket_id: 2,
        price: 1.69,
        pct_change: 0.06,
      },
      {
        supermarket_id: 3,
        price: 1.89,
        pct_change: 0.06,
      },
      {
        supermarket_id: 4,
        price: 1.59,
        pct_change: 0.0,
      },
      {
        supermarket_id: 5,
        price: 1.75,
        pct_change: -0.03,
      },
    ],
  },
  "EGGS-LRG-12CT": {
    history: [
      {
        supermarket_id: 1,
        name: "Eggs (Dozen)",
        price: 2.99,
        created_at: "2025-01-01 08:10:00",
      },
      {
        supermarket_id: 1,
        name: "Eggs (Dozen)",
        price: 3.19,
        created_at: "2025-02-01 08:10:00",
      },
      {
        supermarket_id: 1,
        name: "Eggs (Dozen)",
        price: 3.29,
        created_at: "2025-03-01 08:10:00",
      },
      {
        supermarket_id: 1,
        name: "Eggs (Dozen)",
        price: 3.49,
        created_at: "2025-04-01 08:10:00",
      },
      {
        supermarket_id: 2,
        name: "Eggs (Dozen)",
        price: 2.89,
        created_at: "2025-01-01 09:20:00",
      },
      {
        supermarket_id: 2,
        name: "Eggs (Dozen)",
        price: 3.09,
        created_at: "2025-02-01 09:20:00",
      },
      {
        supermarket_id: 2,
        name: "Eggs (Dozen)",
        price: 3.19,
        created_at: "2025-03-01 09:20:00",
      },
      {
        supermarket_id: 2,
        name: "Eggs (Dozen)",
        price: 3.39,
        created_at: "2025-04-01 09:20:00",
      },
      {
        supermarket_id: 3,
        name: "Eggs (Dozen)",
        price: 3.09,
        created_at: "2025-01-01 10:30:00",
      },
      {
        supermarket_id: 3,
        name: "Eggs (Dozen)",
        price: 3.29,
        created_at: "2025-02-01 10:30:00",
      },
      {
        supermarket_id: 3,
        name: "Eggs (Dozen)",
        price: 3.39,
        created_at: "2025-03-01 10:30:00",
      },
      {
        supermarket_id: 3,
        name: "Eggs (Dozen)",
        price: 3.59,
        created_at: "2025-04-01 10:30:00",
      },
    ],
    product_info: {
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 3.49,
        pct_change: 0.06,
      },
      {
        supermarket_id: 2,
        price: 3.39,
        pct_change: 0.06,
      },
      {
        supermarket_id: 3,
        price: 3.59,
        pct_change: 0.06,
      },
      {
        supermarket_id: 4,
        price: 3.29,
        pct_change: 0.0,
      },
      {
        supermarket_id: 5,
        price: 3.45,
        pct_change: -0.03,
      },
    ],
  },
  "MILK-1L-WHL": {
    history: [
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Liter)",
        price: 1.19,
        created_at: "2025-01-01 08:15:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Liter)",
        price: 1.29,
        created_at: "2025-02-01 08:15:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Liter)",
        price: 1.39,
        created_at: "2025-03-01 08:15:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Liter)",
        price: 1.49,
        created_at: "2025-04-01 08:15:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Liter)",
        price: 1.09,
        created_at: "2025-01-01 09:25:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Liter)",
        price: 1.19,
        created_at: "2025-02-01 09:25:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Liter)",
        price: 1.29,
        created_at: "2025-03-01 09:25:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Liter)",
        price: 1.39,
        created_at: "2025-04-01 09:25:00",
      },
      {
        supermarket_id: 3,
        name: "Whole Milk (1 Liter)",
        price: 1.29,
        created_at: "2025-01-01 10:35:00",
      },
      {
        supermarket_id: 3,
        name: "Whole Milk (1 Liter)",
        price: 1.29,
        created_at: "2025-01-01 10:35:00",
      },
      {
        supermarket_id: 3,
        name: "Whole Milk (1 Liter)",
        price: 1.39,
        created_at: "2025-02-01 10:35:00",
      },
      {
        supermarket_id: 3,
        name: "Whole Milk (1 Liter)",
        price: 1.49,
        created_at: "2025-03-01 10:35:00",
      },
      {
        supermarket_id: 3,
        name: "Whole Milk (1 Liter)",
        price: 1.59,
        created_at: "2025-04-01 10:35:00",
      },
    ],
    product_info: {
      name: "Whole Milk (1 Liter)",
      sku: "MILK-1L-WHL",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 1.49,
        pct_change: 0.07,
      },
      {
        supermarket_id: 2,
        price: 1.39,
        pct_change: 0.08,
      },
      {
        supermarket_id: 3,
        price: 1.59,
        pct_change: 0.07,
      },
      {
        supermarket_id: 4,
        price: 1.29,
        pct_change: 0.0,
      },
      {
        supermarket_id: 5,
        price: 1.45,
        pct_change: -0.03,
      },
    ],
  },
  "FRUIT-BAN-1KG": {
    history: [
      {
        supermarket_id: 1,
        name: "Bananas (1kg)",
        price: 1.29,
        created_at: "2025-01-01 08:20:00",
      },
      {
        supermarket_id: 1,
        name: "Bananas (1kg)",
        price: 1.39,
        created_at: "2025-02-01 08:20:00",
      },
      {
        supermarket_id: 1,
        name: "Bananas (1kg)",
        price: 1.49,
        created_at: "2025-03-01 08:20:00",
      },
      {
        supermarket_id: 1,
        name: "Bananas (1kg)",
        price: 1.59,
        created_at: "2025-04-01 08:20:00",
      },
      {
        supermarket_id: 2,
        name: "Bananas (1kg)",
        price: 1.19,
        created_at: "2025-01-01 09:30:00",
      },
      {
        supermarket_id: 2,
        name: "Bananas (1kg)",
        price: 1.29,
        created_at: "2025-02-01 09:30:00",
      },
      {
        supermarket_id: 2,
        name: "Bananas (1kg)",
        price: 1.39,
        created_at: "2025-03-01 09:30:00",
      },
      {
        supermarket_id: 2,
        name: "Bananas (1kg)",
        price: 1.49,
        created_at: "2025-04-01 09:30:00",
      },
    ],
    product_info: {
      name: "Bananas (1kg)",
      sku: "FRUIT-BAN-1KG",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 1.59,
        pct_change: 0.07,
      },
      {
        supermarket_id: 2,
        price: 1.49,
        pct_change: 0.07,
      },
      {
        supermarket_id: 3,
        price: 1.69,
        pct_change: 0.06,
      },
      {
        supermarket_id: 4,
        price: 1.39,
        pct_change: 0.0,
      },
      {
        supermarket_id: 5,
        price: 1.55,
        pct_change: -0.03,
      },
    ],
  },
  "MILK-1GAL-WHL": {
    history: [
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Gallon)",
        price: 3.29,
        created_at: "2025-01-01 08:05:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Gallon)",
        price: 3.39,
        created_at: "2025-02-01 08:05:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Gallon)",
        price: 3.39,
        created_at: "2025-03-01 08:05:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Gallon)",
        price: 3.49,
        created_at: "2025-04-01 08:05:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Gallon)",
        price: 3.19,
        created_at: "2025-01-01 09:15:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Gallon)",
        price: 3.19,
        created_at: "2025-02-01 09:15:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Gallon)",
        price: 3.29,
        created_at: "2025-03-01 09:15:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Gallon)",
        price: 3.29,
        created_at: "2025-04-01 09:15:00",
      },
    ],
    product_info: {
      name: "Whole Milk (1 Gallon)",
      sku: "MILK-1GAL-WHL",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 3.49,
        pct_change: 0.1,
      },
      {
        supermarket_id: 2,
        price: 3.29,
        pct_change: 0.0,
      },
      {
        supermarket_id: 3,
        price: 3.59,
        pct_change: 0.1,
      },
      {
        supermarket_id: 4,
        price: 3.19,
        pct_change: 0.0,
      },
      {
        supermarket_id: 5,
        price: 3.39,
        pct_change: -0.1,
      },
    ],
  },
}

// Mock price comparison result
export const MOCK_PRICE_COMPARISON: PriceComparisonResult = {
  optimal: [
    {
      supermarket_id: 4,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.49,
      created_at: "2025-04-01 09:35:00",
    },
    {
      supermarket_id: 4,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.09,
      created_at: "2025-04-01 09:40:00",
    },
    {
      supermarket_id: 4,
      name: "Whole Milk (1 Liter)",
      sku: "MILK-1L-WHL",
      price: 1.29,
      created_at: "2025-04-01 09:45:00",
    },
  ],
  best: [
    {
      supermarket_id: 4,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.59,
      created_at: "2025-04-01 09:35:00",
    },
    {
      supermarket_id: 4,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.29,
      created_at: "2025-04-01 09:40:00",
    },
    {
      supermarket_id: 4,
      name: "Whole Milk (1 Liter)",
      sku: "MILK-1L-WHL",
      price: 1.29,
      created_at: "2025-04-01 09:45:00",
    },
  ],
  median: [
    {
      supermarket_id: 5,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.75,
      created_at: "2025-04-01 10:05:00",
    },
    {
      supermarket_id: 5,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.45,
      created_at: "2025-04-01 10:10:00",
    },
    {
      supermarket_id: 5,
      name: "Whole Milk (1 Liter)",
      sku: "MILK-1L-WHL",
      price: 1.45,
      created_at: "2025-04-01 10:15:00",
    },
  ],
  worst: [
    {
      supermarket_id: 3,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.89,
      created_at: "2025-04-01 10:35:00",
    },
    {
      supermarket_id: 3,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.59,
      created_at: "2025-04-01 10:40:00",
    },
    {
      supermarket_id: 3,
      name: "Whole Milk (1 Liter)",
      sku: "MILK-1L-WHL",
      price: 1.59,
      created_at: "2025-04-01 10:45:00",
    },
  ],
}

// Mock inflation result
export const MOCK_INFLATION: InflationResult = {
  global_inflation: {
    mean_inflation: {
      start_price: 2.37,
      end_price: 2.31,
      absolute_change: 0.07,
      inflation_rate: -2.88,
    },
    min_inflation: {
      start_price: 1.41,
      end_price: 1.39,
      absolute_change: 0.02,
      inflation_rate: -1.42,
    },
    gap_inflation: {
      start_price: 1.96,
      end_price: 1.9,
      absolute_change: 0.06,
      inflation_rate: -3.06,
    },
  },
  per_product_inflation: [
    {
      sku: "BREAD-WHT-500G",
      name: "White Bread (500g)",
      inflation_rate: -1.29,
    },
    {
      sku: "EGGS-LRG-12CT",
      name: "Eggs (Dozen)",
      inflation_rate: -3.65,
    },
  ],
}

// Import the types needed for the mock data
import type { ProductListResult, ProductDetailResult, PriceComparisonResult, InflationResult } from "@/lib/api/api"
