"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import Image from "next/image"
import { ArrowLeft, ShoppingCart, Store, Link2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useCart } from "@/hooks/use-cart"
import { API } from "@/lib/api/api"
import type { ProductData } from "@/lib/data/product-data"

export default function ShoppingListPage() {
  const searchParams = useSearchParams()
  const selectedSupermarket = searchParams.get("supermarket")

  const [loading, setLoading] = useState(true)
  const [products, setProducts] = useState<ProductData[]>([])
  const [comparisons, setComparisons] = useState<any>(null)
  const { cart, selectedProducts } = useCart()

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)

        // Load all products
        const allProducts = await API.getProducts()
        setProducts(allProducts)

        // Get selected cart items with quantities
        const selectedItems = cart.filter((item) => selectedProducts.includes(item.productId))

        if (selectedItems.length === 0) {
          setLoading(false)
          return
        }

        // Create a quantities map
        const quantities: Record<string, number> = {}
        selectedItems.forEach((item) => {
          quantities[item.productId] = item.quantity
        })

        // Call the API to get price comparison
        const comparisonData = await API.getPriceComparison(
          selectedItems.map((item) => item.productId),
          quantities,
        )

        setComparisons(comparisonData)
      } catch (error) {
        console.error("Error loading shopping list data:", error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [cart, selectedProducts])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <p>Loading your shopping list...</p>
      </div>
    )
  }

  if (!comparisons) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4">
        <h1 className="text-2xl font-bold">No items selected</h1>
        <p className="text-gray-500">Please select items in your cart to generate a shopping list.</p>
        <Link href="/cart">
          <Button>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Cart
          </Button>
        </Link>
      </div>
    )
  }

  const { optimal, best, average, worst } = comparisons

  // If a specific supermarket is selected, show that shopping list
  if (selectedSupermarket) {
    const supermarketData = [best, average, worst].find((s) => s.name === selectedSupermarket)

    if (!supermarketData) {
      return (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <h1 className="text-2xl font-bold">Supermarket not found</h1>
          <p className="text-gray-500">The selected supermarket could not be found.</p>
          <Link href="/cart">
            <Button>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Cart
            </Button>
          </Link>
        </div>
      )
    }

    return (
      <>
        <div className="mb-6 flex items-center justify-between">
          <Link href="/cart" className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to cart
          </Link>

          <h1 className="text-2xl font-bold">Shopping List: {supermarketData.name}</h1>
        </div>

        <Card>
          <CardHeader className="border-b">
            <CardTitle className="flex items-center justify-between">
              <span>{supermarketData.name}</span>
              <Badge variant="outline">${supermarketData.totalPrice}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {supermarketData.items.map((item: any) => {
                const product = products.find((p) => p.id === item.productId)
                const cartItem = cart.find((c) => c.productId === item.productId)

                if (!product) return null

                return (
                  <div key={item.productId} className="flex items-center border-b pb-4">
                    <div className="h-16 w-16 relative mr-4">
                      <Image
                        src={product.image || "/placeholder.svg"}
                        alt={product.name}
                        fill
                        className="object-contain"
                      />
                    </div>

                    <div className="flex-1">
                      <Link href={`/product/${product.id}`} className="font-medium hover:underline">
                        {product.name}
                      </Link>
                      <div className="text-sm text-gray-500 mt-1">SKU: {product.sku}</div>
                      <div className="text-sm font-medium mt-1">
                        ${item.price} × {cartItem?.quantity || 1} = ${item.total}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Link href={`/product/${product.id}`}>
                        <Button variant="outline" size="sm">
                          View
                        </Button>
                      </Link>
                      <Link href="#" target="_blank" rel="noopener noreferrer">
                        <Button variant="ghost" size="sm">
                          <Link2 className="h-4 w-4" />
                        </Button>
                      </Link>
                    </div>
                  </div>
                )
              })}
            </div>

            <div className="mt-6 p-4 bg-gray-50 rounded-md">
              <div className="flex justify-between items-center">
                <span className="font-medium">Total</span>
                <span className="font-bold">${supermarketData.totalPrice}</span>
              </div>

              <div className="mt-4 flex justify-end">
                <Link href="/cart">
                  <Button size="sm">
                    <ShoppingCart className="h-4 w-4 mr-2" />
                    Back to Cart
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </>
    )
  }

  // Otherwise, show the optimal shopping list
  return (
    <>
      <div className="mb-6 flex items-center justify-between">
        <Link href="/cart" className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to cart
        </Link>

        <h1 className="text-2xl font-bold">Optimal Shopping List</h1>
      </div>

      <Card>
        <CardHeader className="bg-purple-50 border-b border-purple-100">
          <CardTitle className="flex items-center justify-between">
            <span>Optimal Shopping List</span>
            <Badge variant="outline" className="bg-purple-100 text-purple-800">
              ${optimal.totalPrice}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <p className="mb-4 text-sm text-gray-500">
            This shopping list combines products from different supermarkets to get you the best possible price.
          </p>

          {/* Group items by supermarket */}
          {Array.from(new Set(optimal.items.map((item: any) => item.supermarket))).map((supermarket) => (
            <div key={supermarket as string} className="mb-6">
              <h3 className="text-lg font-medium flex items-center mb-3">
                <Store className="h-4 w-4 mr-2" />
                {supermarket as string}
              </h3>

              <div className="space-y-3">
                {optimal.items
                  .filter((item: any) => item.supermarket === supermarket)
                  .map((item: any) => {
                    const product = products.find((p) => p.id === item.productId)
                    const cartItem = cart.find((c) => c.productId === item.productId)

                    if (!product) return null

                    return (
                      <div key={item.productId} className="flex items-center border-b pb-3">
                        <div className="h-12 w-12 relative mr-3">
                          <Image
                            src={product.image || "/placeholder.svg"}
                            alt={product.name}
                            fill
                            className="object-contain"
                          />
                        </div>

                        <div className="flex-1">
                          <Link href={`/product/${product.id}`} className="font-medium hover:underline">
                            {product.name}
                          </Link>
                          <div className="text-sm text-gray-500">
                            ${item.price} × {cartItem?.quantity || 1} = ${item.total}
                          </div>
                        </div>

                        <div className="flex gap-2">
                          <Link href={`/product/${product.id}`}>
                            <Button variant="outline" size="sm">
                              View
                            </Button>
                          </Link>
                          <Link href="#" target="_blank" rel="noopener noreferrer">
                            <Button variant="ghost" size="sm">
                              <Link2 className="h-4 w-4" />
                            </Button>
                          </Link>
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>
          ))}

          <div className="mt-6 p-3 bg-gray-50 rounded-md text-sm">
            <p className="font-medium">Total: ${optimal.totalPrice}</p>
            <p className="text-gray-500 text-xs mt-1">
              This is ${best.totalPrice - optimal.totalPrice} less than shopping at the best single supermarket.
            </p>
          </div>
        </CardContent>
      </Card>
    </>
  )
}
