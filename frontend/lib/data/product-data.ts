// Mock data for demonstration
export const mockProducts = {
  milk: {
    id: "1",
    name: "Whole Milk (1 Gallon)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "MILK-1GAL-WHL",
    description: "Fresh whole milk, pasteurized and homogenized.",
    currentPrices: {
      "Supermarket A": 3.49,
      "Supermarket B": 3.29,
      "Supermarket C": 3.59,
      "Supermarket D": 3.19,
      "Supermarket E": 3.39,
    },
    priceChanges: {
      "Supermarket A": 0.1,
      "Supermarket B": 0.0,
      "Supermarket C": 0.1,
      "Supermarket D": 0.0,
      "Supermarket E": -0.1,
    },
    lowestPrice: {
      price: 3.19,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 3.29,
        "Supermarket B": 3.19,
        "Supermarket C": 3.49,
        "Supermarket D": 3.09,
        "Supermarket E": 3.29,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 3.39,
        "Supermarket B": 3.19,
        "Supermarket C": 3.49,
        "Supermarket D": 3.09,
        "Supermarket E": 3.29,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 3.39,
        "Supermarket B": 3.29,
        "Supermarket C": 3.49,
        "Supermarket D": 3.19,
        "Supermarket E": 3.39,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 3.49,
        "Supermarket B": 3.29,
        "Supermarket C": 3.59,
        "Supermarket D": 3.19,
        "Supermarket E": 3.39,
      },
    ],
  },
  apples: {
    id: "2",
    name: "Apples (1lb)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "FRUIT-APL-1LB",
    description: "Fresh red apples, sold by the pound.",
    currentPrices: {
      "Supermarket A": 1.49,
      "Supermarket B": 1.29,
      "Supermarket C": 1.59,
      "Supermarket D": 1.19,
      "Supermarket E": 1.39,
    },
    priceChanges: {
      "Supermarket A": 0.0,
      "Supermarket B": -0.1,
      "Supermarket C": 0.1,
      "Supermarket D": 0.0,
      "Supermarket E": 0.0,
    },
    lowestPrice: {
      price: 1.19,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 1.49,
        "Supermarket B": 1.39,
        "Supermarket C": 1.49,
        "Supermarket D": 1.19,
        "Supermarket E": 1.39,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 1.49,
        "Supermarket B": 1.39,
        "Supermarket C": 1.49,
        "Supermarket D": 1.19,
        "Supermarket E": 1.39,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 1.49,
        "Supermarket B": 1.39,
        "Supermarket C": 1.49,
        "Supermarket D": 1.19,
        "Supermarket E": 1.39,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 1.49,
        "Supermarket B": 1.29,
        "Supermarket C": 1.59,
        "Supermarket D": 1.19,
        "Supermarket E": 1.39,
      },
    ],
  },
  bread: {
    id: "3",
    name: "White Bread (24oz)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "BREAD-WHT-24OZ",
    description: "Soft white bread, perfect for sandwiches and toast.",
    currentPrices: {
      "Supermarket A": 2.49,
      "Supermarket B": 2.29,
      "Supermarket C": 2.59,
      "Supermarket D": 2.19,
      "Supermarket E": 2.39,
    },
    priceChanges: {
      "Supermarket A": -0.05,
      "Supermarket B": 0.1,
      "Supermarket C": 0.1,
      "Supermarket D": 0.0,
      "Supermarket E": 0.0,
    },
    lowestPrice: {
      price: 2.19,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 2.29,
        "Supermarket B": 2.19,
        "Supermarket C": 2.49,
        "Supermarket D": 2.09,
        "Supermarket E": 2.29,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 2.39,
        "Supermarket B": 2.19,
        "Supermarket C": 2.49,
        "Supermarket D": 2.09,
        "Supermarket E": 2.29,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 2.39,
        "Supermarket B": 2.29,
        "Supermarket C": 2.49,
        "Supermarket D": 2.19,
        "Supermarket E": 2.39,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 2.49,
        "Supermarket B": 2.29,
        "Supermarket C": 2.59,
        "Supermarket D": 2.19,
        "Supermarket E": 2.39,
      },
    ],
  },
  bananas: {
    id: "4",
    name: "Bananas (1lb)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "FRUIT-BAN-1LB",
    description: "Fresh yellow bananas, sold by the pound.",
    currentPrices: {
      "Supermarket A": 0.59,
      "Supermarket B": 0.55,
      "Supermarket C": 0.65,
      "Supermarket D": 0.49,
      "Supermarket E": 0.59,
    },
    priceChanges: {
      "Supermarket A": 0.0,
      "Supermarket B": -0.05,
      "Supermarket C": 0.06,
      "Supermarket D": 0.0,
      "Supermarket E": 0.0,
    },
    lowestPrice: {
      price: 0.49,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 0.55,
        "Supermarket B": 0.49,
        "Supermarket C": 0.59,
        "Supermarket D": 0.45,
        "Supermarket E": 0.55,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 0.55,
        "Supermarket B": 0.49,
        "Supermarket C": 0.59,
        "Supermarket D": 0.45,
        "Supermarket E": 0.55,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 0.59,
        "Supermarket B": 0.55,
        "Supermarket C": 0.59,
        "Supermarket D": 0.49,
        "Supermarket E": 0.59,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 0.59,
        "Supermarket B": 0.55,
        "Supermarket C": 0.65,
        "Supermarket D": 0.49,
        "Supermarket E": 0.59,
      },
    ],
  },
  coffee: {
    id: "5",
    name: "Ground Coffee (12oz)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "COFFEE-GRD-12OZ",
    description: "Medium roast ground coffee, perfect for drip coffee makers.",
    currentPrices: {
      "Supermarket A": 8.99,
      "Supermarket B": 8.49,
      "Supermarket C": 9.29,
      "Supermarket D": 7.99,
      "Supermarket E": 8.79,
    },
    priceChanges: {
      "Supermarket A": 0.2,
      "Supermarket B": 0.2,
      "Supermarket C": -0.1,
      "Supermarket D": 0.2,
      "Supermarket E": 0.2,
    },
    lowestPrice: {
      price: 7.99,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 8.49,
        "Supermarket B": 7.99,
        "Supermarket C": 8.99,
        "Supermarket D": 7.49,
        "Supermarket E": 8.29,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 8.49,
        "Supermarket B": 7.99,
        "Supermarket C": 8.99,
        "Supermarket D": 7.49,
        "Supermarket E": 8.29,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 8.79,
        "Supermarket B": 8.29,
        "Supermarket C": 9.19,
        "Supermarket D": 7.79,
        "Supermarket E": 8.59,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 8.99,
        "Supermarket B": 8.49,
        "Supermarket C": 9.29,
        "Supermarket D": 7.99,
        "Supermarket E": 8.79,
      },
    ],
  },
  eggs: {
    id: "6",
    name: "Large Eggs (Dozen)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "EGGS-LRG-12CT",
    description: "Farm fresh large grade A eggs.",
    currentPrices: {
      "Supermarket A": 3.99,
      "Supermarket B": 3.79,
      "Supermarket C": 4.09,
      "Supermarket D": 3.69,
      "Supermarket E": 3.89,
    },
    priceChanges: {
      "Supermarket A": 0.1,
      "Supermarket B": 0.0,
      "Supermarket C": 0.1,
      "Supermarket D": -0.15,
      "Supermarket E": 0.0,
    },
    lowestPrice: {
      price: 3.69,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 3.79,
        "Supermarket B": 3.69,
        "Supermarket C": 3.99,
        "Supermarket D": 3.59,
        "Supermarket E": 3.79,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 3.89,
        "Supermarket B": 3.69,
        "Supermarket C": 3.99,
        "Supermarket D": 3.59,
        "Supermarket E": 3.79,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 3.89,
        "Supermarket B": 3.79,
        "Supermarket C": 3.99,
        "Supermarket D": 3.69,
        "Supermarket E": 3.89,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 3.99,
        "Supermarket B": 3.79,
        "Supermarket C": 4.09,
        "Supermarket D": 3.69,
        "Supermarket E": 3.89,
      },
    ],
  },
  cereal: {
    id: "7",
    name: "Breakfast Cereal (18oz)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "CEREAL-BRKFST-18OZ",
    description: "Crunchy whole grain breakfast cereal with added vitamins and minerals.",
    currentPrices: {
      "Supermarket A": 4.29,
      "Supermarket B": 3.99,
      "Supermarket C": 4.49,
      "Supermarket D": 3.89,
      "Supermarket E": 4.19,
    },
    priceChanges: {
      "Supermarket A": 0.0,
      "Supermarket B": -0.2,
      "Supermarket C": 0.1,
      "Supermarket D": 0.0,
      "Supermarket E": 0.0,
    },
    lowestPrice: {
      price: 3.89,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 4.29,
        "Supermarket B": 4.19,
        "Supermarket C": 4.39,
        "Supermarket D": 3.89,
        "Supermarket E": 4.19,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 4.29,
        "Supermarket B": 4.19,
        "Supermarket C": 4.39,
        "Supermarket D": 3.89,
        "Supermarket E": 4.19,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 4.29,
        "Supermarket B": 4.19,
        "Supermarket C": 4.39,
        "Supermarket D": 3.89,
        "Supermarket E": 4.19,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 4.29,
        "Supermarket B": 3.99,
        "Supermarket C": 4.49,
        "Supermarket D": 3.89,
        "Supermarket E": 4.19,
      },
    ],
  },
  detergent: {
    id: "8",
    name: "Laundry Detergent (100oz)",
    image: "/placeholder.svg?height=200&width=200",
    sku: "LAUNDRY-DET-100OZ",
    description: "Concentrated liquid laundry detergent, enough for 64 loads.",
    currentPrices: {
      "Supermarket A": 11.99,
      "Supermarket B": 10.99,
      "Supermarket C": 12.49,
      "Supermarket D": 10.49,
      "Supermarket E": 11.79,
    },
    priceChanges: {
      "Supermarket A": 0.5,
      "Supermarket B": 0.0,
      "Supermarket C": 0.0,
      "Supermarket D": -0.5,
      "Supermarket E": 0.3,
    },
    lowestPrice: {
      price: 10.49,
      store: "Supermarket D",
    },
    priceHistory: [
      {
        date: "Jan 2024",
        "Supermarket A": 11.49,
        "Supermarket B": 10.99,
        "Supermarket C": 12.49,
        "Supermarket D": 10.99,
        "Supermarket E": 11.49,
      },
      {
        date: "Feb 2024",
        "Supermarket A": 11.49,
        "Supermarket B": 10.99,
        "Supermarket C": 12.49,
        "Supermarket D": 10.99,
        "Supermarket E": 11.49,
      },
      {
        date: "Mar 2024",
        "Supermarket A": 11.49,
        "Supermarket B": 10.99,
        "Supermarket C": 12.49,
        "Supermarket D": 10.99,
        "Supermarket E": 11.49,
      },
      {
        date: "Apr 2024",
        "Supermarket A": 11.99,
        "Supermarket B": 10.99,
        "Supermarket C": 12.49,
        "Supermarket D": 10.49,
        "Supermarket E": 11.79,
      },
    ],
  },
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

// Extended mock products list for API
export const EXTENDED_MOCK_PRODUCTS = [
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
    name: "Ground Coffee (250g)",
    sku: "COFFEE-GRD-250G",
  },
  {
    id: 68,
    name: "Cheddar Cheese (200g)",
    sku: "CHEESE-CHED-200G",
  },
  {
    id: 1,
    name: "Whole Milk (1 Gallon)",
    sku: "MILK-1GAL-WHL",
  },
  {
    id: 2,
    name: "Apples (1lb)",
    sku: "FRUIT-APL-1LB",
  },
  {
    id: 3,
    name: "White Bread (24oz)",
    sku: "BREAD-WHT-24OZ",
  },
  {
    id: 4,
    name: "Bananas (1lb)",
    sku: "FRUIT-BAN-1LB",
  },
  {
    id: 5,
    name: "Ground Coffee (12oz)",
    sku: "COFFEE-GRD-12OZ",
  },
  {
    id: 6,
    name: "Large Eggs (Dozen)",
    sku: "EGGS-LRG-12CT",
  },
  {
    id: 7,
    name: "Breakfast Cereal (18oz)",
    sku: "CEREAL-BRKFST-18OZ",
  },
  {
    id: 8,
    name: "Laundry Detergent (100oz)",
    sku: "LAUNDRY-DET-100OZ",
  },
]

// Mock product detail for fallback
export const MOCK_PRODUCT_DETAILS: Record<string, any> = {
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
export const MOCK_PRICE_COMPARISON = {
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
export const MOCK_INFLATION = {
  mean: 6.55,
  min: 7.19,
  gap: 0.64,
}
