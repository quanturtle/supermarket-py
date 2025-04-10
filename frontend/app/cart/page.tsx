"use client"

import { useEffect } from "react"
import { useCart } from "@/hooks/use-cart"

// Import our consolidated components
import { CartHeader, CartCard, CartComparisonCard } from "@/components/cart/cart-components"

export default function CartPage() {
  const {
    cart,
    selectedProducts,
    products,
    comparing,
    comparisonResults,
    updateQuantity,
    removeFromCart,
    clearCart,
    toggleProductSelection,
    selectAllProducts,
    deselectAllProducts,
    getCartItems,
    compareCartPrices,
    loadProducts,
  } = useCart()

  // Ensure products are loaded
  useEffect(() => {
    loadProducts()
  }, [loadProducts])

  const cartItems = getCartItems()
  const isCompareDisabled = selectedProducts.length === 0 || comparing

  return (
    <>
      <CartHeader
        cartItemsCount={cartItems.length}
        onClearCart={clearCart}
        onCompareCartPrices={compareCartPrices}
        isCompareDisabled={isCompareDisabled}
      />

      {/* Cart at the top */}
      <CartCard
        cartItems={cartItems}
        selectedProducts={selectedProducts}
        onToggleSelect={toggleProductSelection}
        onUpdateQuantity={updateQuantity}
        onRemove={removeFromCart}
        onSelectAll={selectAllProducts}
        onDeselectAll={deselectAllProducts}
        onCompare={compareCartPrices}
        isCompareDisabled={isCompareDisabled}
      />

      {/* Comparison cards in a row */}
      <CartComparisonCard
        comparing={comparing}
        comparisonResults={comparisonResults}
        products={products}
        cart={cart}
        onCompare={compareCartPrices}
        isCompareDisabled={isCompareDisabled}
      />
    </>
  )
}
