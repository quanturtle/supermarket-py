"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

type CartItem = {
  productId: string
  quantity: number
}

interface CartContextType {
  cart: CartItem[]
  selectedProducts: string[]
  addToCart: (productId: string, quantity: number) => void
  updateQuantity: (productId: string, quantity: number) => void
  removeFromCart: (productId: string) => void
  clearCart: () => void
  toggleProductSelection: (productId: string) => void
  selectAllProducts: () => void
  deselectAllProducts: () => void
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<CartItem[]>([])
  const [selectedProducts, setSelectedProducts] = useState<string[]>([])

  // Load cart from localStorage on initial render
  useEffect(() => {
    const savedCart = localStorage.getItem("priceTrackerCart")
    if (savedCart) {
      try {
        const parsedCart = JSON.parse(savedCart)
        setCart(parsedCart)
        setSelectedProducts(parsedCart.map((item: CartItem) => item.productId))
      } catch (e) {
        console.error("Error loading cart from localStorage", e)
      }
    } else {
      // Add some sample items to the cart for demonstration
      const initialCart = [
        { productId: "1", quantity: 2 }, // Milk
        { productId: "3", quantity: 1 }, // Bread
        { productId: "6", quantity: 1 }, // Eggs
      ]
      setCart(initialCart)
      setSelectedProducts(initialCart.map((item) => item.productId))
    }
  }, [])

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    if (cart.length > 0) {
      localStorage.setItem("priceTrackerCart", JSON.stringify(cart))
    }
  }, [cart])

  const addToCart = (productId: string, quantity = 1) => {
    setCart((prevCart) => {
      const existingItem = prevCart.find((item) => item.productId === productId)
      if (existingItem) {
        return prevCart.map((item) =>
          item.productId === productId ? { ...item, quantity: item.quantity + quantity } : item,
        )
      } else {
        return [...prevCart, { productId, quantity }]
      }
    })

    // Add to selected products if not already there
    setSelectedProducts((prev) => (prev.includes(productId) ? prev : [...prev, productId]))
  }

  const updateQuantity = (productId: string, newQuantity: number) => {
    if (newQuantity < 1) {
      removeFromCart(productId)
      return
    }

    setCart((prevCart) =>
      prevCart.map((item) => (item.productId === productId ? { ...item, quantity: newQuantity } : item)),
    )
  }

  const removeFromCart = (productId: string) => {
    setCart((prevCart) => prevCart.filter((item) => item.productId !== productId))
    setSelectedProducts((prev) => prev.filter((id) => id !== productId))
  }

  const clearCart = () => {
    setCart([])
    setSelectedProducts([])
    localStorage.removeItem("priceTrackerCart")
  }

  const toggleProductSelection = (productId: string) => {
    setSelectedProducts((prev) =>
      prev.includes(productId) ? prev.filter((id) => id !== productId) : [...prev, productId],
    )
  }

  const selectAllProducts = () => {
    setSelectedProducts(cart.map((item) => item.productId))
  }

  const deselectAllProducts = () => {
    setSelectedProducts([])
  }

  return (
    <CartContext.Provider
      value={{
        cart,
        selectedProducts,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        toggleProductSelection,
        selectAllProducts,
        deselectAllProducts,
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

