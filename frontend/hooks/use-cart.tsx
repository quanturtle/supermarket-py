"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { API, type ProductListResult, type PriceComparisonResult, type ShoppingListItem } from "@/lib/api/api"

// Define cart item type
export type CartItem = {
  sku: string
  quantity: number
}

interface CartContextType {
  cart: CartItem[]
  selectedProducts: string[]
  products: ProductListResult[]
  comparing: boolean
  comparisonResults: PriceComparisonResult | null
  addToCart: (sku: string, quantity: number) => void
  updateQuantity: (sku: string, quantity: number) => void
  removeFromCart: (sku: string) => void
  clearCart: () => void
  toggleProductSelection: (sku: string) => void
  selectAllProducts: () => void
  deselectAllProducts: () => void
  getCartItems: () => Array<{ sku: string; quantity: number; product: ProductListResult | undefined }>
  compareCartPrices: () => Promise<void>
  loadProducts: () => Promise<void>
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<CartItem[]>([])
  const [selectedProducts, setSelectedProducts] = useState<string[]>([])
  const [products, setProducts] = useState<ProductListResult[]>([])
  const [comparing, setComparing] = useState(false)
  const [comparisonResults, setComparisonResults] = useState<PriceComparisonResult | null>(null)
  const [productsLoaded, setProductsLoaded] = useState(false)

  // Load cart from localStorage on initial render
  useEffect(() => {
    const savedCart = getCart()
    setCart(savedCart)

    const savedSelected = getSelectedProducts()
    setSelectedProducts(savedSelected)

    // Load products
    loadProducts()
  }, [])

  // Cart functions using localStorage
  const getCart = (): CartItem[] => {
    try {
      const cartJson = localStorage.getItem("priceTrackerCart")
      return cartJson ? JSON.parse(cartJson) : []
    } catch (error) {
      console.error("Error getting cart from localStorage:", error)
      return []
    }
  }

  const addToCartLocal = (sku: string, quantity: number): boolean => {
    try {
      // Get current cart from localStorage
      const cartJson = localStorage.getItem("priceTrackerCart")
      let cart = []

      if (cartJson) {
        cart = JSON.parse(cartJson)
        // Check if product already exists in cart
        const existingItemIndex = cart.findIndex((item: any) => item.sku === sku)

        if (existingItemIndex >= 0) {
          // Update quantity if product already in cart
          cart[existingItemIndex].quantity += quantity
        } else {
          // Add new item to cart
          cart.push({ sku, quantity })
        }
      } else {
        // Create new cart with this product
        cart = [{ sku, quantity }]
      }

      // Save updated cart to localStorage
      localStorage.setItem("priceTrackerCart", JSON.stringify(cart))

      return true
    } catch (error) {
      console.error("Error adding to cart:", error)
      return false
    }
  }

  const updateCartItemQuantityLocal = (sku: string, quantity: number): boolean => {
    try {
      const cart = getCart()
      const updatedCart = cart.map((item) => (item.sku === sku ? { ...item, quantity } : item))
      localStorage.setItem("priceTrackerCart", JSON.stringify(updatedCart))
      return true
    } catch (error) {
      console.error("Error updating cart item quantity:", error)
      return false
    }
  }

  const removeFromCartLocal = (sku: string): boolean => {
    try {
      const cart = getCart()
      const updatedCart = cart.filter((item) => item.sku !== sku)
      localStorage.setItem("priceTrackerCart", JSON.stringify(updatedCart))
      return true
    } catch (error) {
      console.error("Error removing item from cart:", error)
      return false
    }
  }

  const clearCartLocal = (): boolean => {
    try {
      localStorage.removeItem("priceTrackerCart")
      return true
    } catch (error) {
      console.error("Error clearing cart:", error)
      return false
    }
  }

  const getSelectedProducts = (): string[] => {
    try {
      const selectedJson = localStorage.getItem("priceTrackerSelectedProducts")
      return selectedJson ? JSON.parse(selectedJson) : []
    } catch (error) {
      console.error("Error getting selected products:", error)
      return []
    }
  }

  const setSelectedProductsLocal = (skus: string[]): boolean => {
    try {
      localStorage.setItem("priceTrackerSelectedProducts", JSON.stringify(skus))
      return true
    } catch (error) {
      console.error("Error setting selected products:", error)
      return false
    }
  }

  const toggleProductSelectionLocal = (sku: string): { success: boolean; selected: boolean } => {
    try {
      const selected = getSelectedProducts()
      let newSelected: string[]
      let isSelected: boolean

      if (selected.includes(sku)) {
        newSelected = selected.filter((id) => id !== sku)
        isSelected = false
      } else {
        newSelected = [...selected, sku]
        isSelected = true
      }

      localStorage.setItem("priceTrackerSelectedProducts", JSON.stringify(newSelected))
      return { success: true, selected: isSelected }
    } catch (error) {
      console.error("Error toggling product selection:", error)
      return { success: false, selected: false }
    }
  }

  const selectAllProductsLocal = (): boolean => {
    try {
      const cart = getCart()
      const allSkus = cart.map((item) => item.sku)
      localStorage.setItem("priceTrackerSelectedProducts", JSON.stringify(allSkus))
      return true
    } catch (error) {
      console.error("Error selecting all products:", error)
      return false
    }
  }

  const deselectAllProductsLocal = (): boolean => {
    try {
      localStorage.setItem("priceTrackerSelectedProducts", JSON.stringify([]))
      return true
    } catch (error) {
      console.error("Error deselecting all products:", error)
      return false
    }
  }

  // API and state functions
  const loadProducts = async () => {
    if (productsLoaded) return

    try {
      const allProducts = await API.getAllProducts()
      setProducts(allProducts)
      setProductsLoaded(true)
    } catch (error) {
      console.error("Error loading products:", error)
    }
  }

  const addToCart = (sku: string, quantity = 1) => {
    // First update localStorage
    const success = addToCartLocal(sku, quantity)

    if (success) {
      // Then update state
      setCart(getCart())

      // Add to selected products if not already there
      if (!selectedProducts.includes(sku)) {
        const newSelected = [...selectedProducts, sku]
        setSelectedProducts(newSelected)
        setSelectedProductsLocal(newSelected)
      }

      return true
    }

    return false
  }

  const updateQuantity = (sku: string, newQuantity: number) => {
    if (newQuantity < 1) {
      removeFromCart(sku)
      return
    }

    updateCartItemQuantityLocal(sku, newQuantity)
    setCart(getCart())
  }

  const removeFromCart = (sku: string) => {
    removeFromCartLocal(sku)
    setCart(getCart())

    // Also remove from selected products
    if (selectedProducts.includes(sku)) {
      const newSelected = selectedProducts.filter((id) => id !== sku)
      setSelectedProducts(newSelected)
      setSelectedProductsLocal(newSelected)
    }
  }

  const clearCart = () => {
    clearCartLocal()
    deselectAllProductsLocal()
    setCart([])
    setSelectedProducts([])
    setComparisonResults(null)
  }

  const toggleProductSelection = (sku: string) => {
    const result = toggleProductSelectionLocal(sku)
    setSelectedProducts(getSelectedProducts())
  }

  const selectAllProducts = () => {
    selectAllProductsLocal()
    setSelectedProducts(getSelectedProducts())
  }

  const deselectAllProducts = () => {
    deselectAllProductsLocal()
    setSelectedProducts([])
  }

  const getCartItems = () => {
    return cart
      .map((item) => {
        const product = products.find((p) => p.sku === item.sku)
        return {
          ...item,
          product,
        }
      })
      .filter((item) => item.product) // Filter out any items where product wasn't found
  }

  const compareCartPrices = async () => {
    if (selectedProducts.length === 0) {
      alert("Please select at least one product to compare")
      return
    }

    setComparing(true)
    try {
      // Get selected cart items with quantities
      const selectedItems = cart.filter((item) => selectedProducts.includes(item.sku))

      // Create shopping list for API
      const shoppingList: ShoppingListItem[] = selectedItems.map((item) => ({
        sku: item.sku,
        quantity: item.quantity,
      }))

      // Call the API to get price comparison
      const comparisons = await API.getPriceComparison(shoppingList)
      setComparisonResults(comparisons)
    } catch (error) {
      console.error("Error comparing prices:", error)
      alert("An error occurred while comparing prices")
    } finally {
      setComparing(false)
    }
  }

  return (
    <CartContext.Provider
      value={{
        cart,
        selectedProducts,
        products,
        comparing,
        comparisonResults,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        toggleProductSelection,
        selectAllProducts,
        deselectAllProducts,
        getCartItems,
        compareCartPrices,
        loadProducts,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider")
  }
  return context
}
