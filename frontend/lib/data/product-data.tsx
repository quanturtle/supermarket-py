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

// Function to simulate an API call
export async function getMockProducts(): Promise<typeof mockProducts> {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    // Return the mock data
    return mockProducts
}

// Function to get a single product by ID
export async function getMockProductById(id: string): Promise<ProductData | null> {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    // Find the product with the matching ID
    const product = Object.values(mockProducts).find((product) => product.id === id)

    return product || null
}

// Function to get all products as an array
export async function getAllProducts(): Promise<ProductData[]> {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    // Convert the object to an array and sort by name
    return Object.values(mockProducts).sort((a, b) => a.name.localeCompare(b.name))
}

// Function to get a single product by slug (name)
export async function getMockProductBySlug(slug: string): Promise<ProductData | null> {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    // Find the product with the matching name (slug)
    const product = Object.values(mockProducts).find(
        (product) => product.name.toLowerCase().replace(/[^a-z0-9]+/g, "-") === slug,
    )

    return product || null
}

