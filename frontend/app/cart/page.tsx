"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { ProductData } from "@/lib/data/product-data"
import { ShoppingCart } from "lucide-react"
import { useCart } from "@/hooks/use-cart"
import { API } from "@/lib/api/api"

// Import our modular components
import { CartHeader } from "@/components/cart/cart-header"
import { CartItemsList } from "@/components/cart/cart-items-list"
import { EmptyCartMessage } from "@/components/cart/empty-cart-message"
import { PriceComparisonGrid } from "@/components/cart/price-comparison-grid"

type SupermarketPricing = {
    name: string
    totalPrice: number
    items: {
        productId: string
        price: number
        total: number
    }[]
}

export default function CartPage() {
    const [products, setProducts] = useState<ProductData[]>([])
    const [loading, setLoading] = useState(true)
    const [comparing, setComparing] = useState(false)
    const [supermarketComparisons, setSupermarketComparisons] = useState<{
        worst: SupermarketPricing
        average: SupermarketPricing
        best: SupermarketPricing
        optimal: {
            totalPrice: number
            items: {
                productId: string
                supermarket: string
                price: number
                total: number
            }[]
        }
    } | null>(null)

    const {
        cart,
        selectedProducts,
        updateQuantity,
        removeFromCart,
        clearCart,
        toggleProductSelection,
        selectAllProducts,
        deselectAllProducts,
    } = useCart()

    useEffect(() => {
        async function loadProducts() {
            try {
                const allProducts = await API.getAllProducts()
                setProducts(allProducts)
            } catch (error) {
                console.error("Error loading products:", error)
            } finally {
                setLoading(false)
            }
        }

        loadProducts()
    }, [])

    const getCartItems = () => {
        return cart
            .map((item) => {
                const product = products.find((p) => p.id === item.productId)
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
            const selectedItems = cart.filter((item) => selectedProducts.includes(item.productId))

            // Create a quantities map
            const quantities: Record<string, number> = {}
            selectedItems.forEach((item) => {
                quantities[item.productId] = item.quantity
            })

            const comparisons = await API.getPriceComparison(
                selectedItems.map((item) => item.productId),
                quantities,
            )

            setSupermarketComparisons(comparisons)
        } catch (error) {
            console.error("Error comparing prices:", error)
            alert("An error occurred while comparing prices")
        } finally {
            setComparing(false)
        }
    }

    if (loading) {
        return (
            <div className="container flex items-center justify-center min-h-screen">
                <p>Loading cart...</p>
            </div>
        )
    }

    const cartItems = getCartItems()

    return (
        <>
            <CartHeader
                cartItemsCount={cartItems.length}
                onClearCart={clearCart}
                onCompareCartPrices={compareCartPrices}
                isCompareDisabled={selectedProducts.length === 0 || comparing}
            />

            {/* Cart at the top */}
            <Card className="mb-6">
                <CardHeader>
                    <CardTitle>Your Cart ({cartItems.length})</CardTitle>
                    <CardDescription>Select which items to include in your comparison</CardDescription>
                </CardHeader>
                <CardContent>
                    {cart.length === 0 ? (
                        <EmptyCartMessage onCompare={compareCartPrices} isDisabled={selectedProducts.length === 0 || comparing} />
                    ) : (
                        <CartItemsList
                            cartItems={cartItems}
                            selectedProducts={selectedProducts}
                            onToggleSelect={toggleProductSelection}
                            onUpdateQuantity={updateQuantity}
                            onRemove={removeFromCart}
                            onSelectAll={selectAllProducts}
                            onDeselectAll={deselectAllProducts}
                        />
                    )}
                </CardContent>
            </Card>

            {/* Comparison cards in a row */}
            {comparing ? (
                <Card className="h-full flex items-center justify-center">
                    <CardContent className="py-12 text-center">
                        <div className="animate-pulse">
                            <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <h2 className="text-xl font-semibold mb-2">Comparing Prices...</h2>
                            <p className="text-gray-500 max-w-md mx-auto">
                                We're calculating the best deals across all supermarkets.
                            </p>
                        </div>
                    </CardContent>
                </Card>
            ) : supermarketComparisons ? (
                <PriceComparisonGrid comparisons={supermarketComparisons} products={products} cart={cart} />
            ) : (
                <Card className="h-full flex items-center justify-center">
                    <CardContent className="py-12 text-center">
                        <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                        <h2 className="text-xl font-semibold mb-2">Ready to Compare</h2>
                        <p className="text-gray-500 max-w-md mx-auto mb-6">
                            Add products to your cart using the search button above, then click "Compare Prices" to see which
                            supermarket offers the best deals.
                        </p>
                        <Button onClick={compareCartPrices} disabled={selectedProducts.length === 0 || comparing}>
                            Compare Prices
                        </Button>
                    </CardContent>
                </Card>
            )}
        </>
    )
}