// Mock products
export const MOCK_PRODUCTS = [
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
    id: 55,
    name: "Whole Milk (1 Gallon)",
    sku: "MILK-1GAL-WHL",
  },
]

// Mock product details
export const MOCK_PRODUCT_DETAILS: Record<string, any> = {
  "BREAD-WHT-500G": {
    history: [
      {
        supermarket_id: 1,
        name: "White Bread (500g)",
        price: 1.49,
        created_at: "2025-01-01T08:05:00",
      },
      {
        supermarket_id: 1,
        name: "White Bread (500g)",
        price: 1.59,
        created_at: "2025-02-01T08:05:00",
      },
      {
        supermarket_id: 2,
        name: "White Bread (500g)",
        price: 1.59,
        created_at: "2025-01-01T08:35:00",
      },
      {
        supermarket_id: 2,
        name: "White Bread (500g)",
        price: 1.69,
        created_at: "2025-02-01T08:35:00",
      },
    ],
    product_info: {
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 1.49,
        pct_change: 2.0,
      },
      {
        supermarket_id: 2,
        price: 1.59,
        pct_change: 0.0,
      },
    ],
  },
  "EGGS-LRG-12CT": {
    history: [
      {
        supermarket_id: 1,
        name: "Eggs (Dozen)",
        price: 3.29,
        created_at: "2025-01-01T08:10:00",
      },
      {
        supermarket_id: 1,
        name: "Eggs (Dozen)",
        price: 3.19,
        created_at: "2025-02-01T08:10:00",
      },
      {
        supermarket_id: 2,
        name: "Eggs (Dozen)",
        price: 3.39,
        created_at: "2025-01-01T08:40:00",
      },
      {
        supermarket_id: 2,
        name: "Eggs (Dozen)",
        price: 3.29,
        created_at: "2025-02-01T08:40:00",
      },
    ],
    product_info: {
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 3.29,
        pct_change: -3.0,
      },
      {
        supermarket_id: 2,
        price: 3.39,
        pct_change: -2.9,
      },
    ],
  },
  "MILK-1L-WHL": {
    history: [
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Liter)",
        price: 1.19,
        created_at: "2025-01-01T08:15:00",
      },
      {
        supermarket_id: 1,
        name: "Whole Milk (1 Liter)",
        price: 1.29,
        created_at: "2025-02-01T08:15:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Liter)",
        price: 1.29,
        created_at: "2025-01-01T08:45:00",
      },
      {
        supermarket_id: 2,
        name: "Whole Milk (1 Liter)",
        price: 1.39,
        created_at: "2025-02-01T08:45:00",
      },
    ],
    product_info: {
      name: "Whole Milk (1 Liter)",
      sku: "MILK-1L-WHL",
    },
    price_changes: [
      {
        supermarket_id: 1,
        price: 1.19,
        pct_change: 8.4,
      },
      {
        supermarket_id: 2,
        price: 1.29,
        pct_change: 7.8,
      },
    ],
  },
}

// Mock price comparison
export const MOCK_PRICE_COMPARISON = {
  optimal: [
    {
      supermarket_id: 4,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.49,
      created_at: "2025-02-01T09:35:00",
    },
    {
      supermarket_id: 4,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.09,
      created_at: "2025-02-01T09:40:00",
    },
  ],
  best: [
    {
      supermarket_id: 4,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.49,
      created_at: "2025-02-01T09:35:00",
    },
    {
      supermarket_id: 4,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.09,
      created_at: "2025-02-01T09:40:00",
    },
  ],
  median: [
    {
      supermarket_id: 5,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.65,
      created_at: "2025-02-01T10:05:00",
    },
    {
      supermarket_id: 5,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.25,
      created_at: "2025-02-01T10:10:00",
    },
  ],
  worst: [
    {
      supermarket_id: 6,
      name: "White Bread (500g)",
      sku: "BREAD-WHT-500G",
      price: 1.79,
      created_at: "2025-02-01T10:35:00",
    },
    {
      supermarket_id: 6,
      name: "Eggs (Dozen)",
      sku: "EGGS-LRG-12CT",
      price: 3.49,
      created_at: "2025-02-01T10:40:00",
    },
  ],
}

// Mock inflation data
export const MOCK_INFLATION = {
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

// Mock date range for inflation calculator
export const MOCK_DATE_RANGE = {
  start_date: "2025-01-01",
  end_date: "2025-04-09",
}
