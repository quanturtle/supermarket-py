"use client"

import { useEffect, useState } from "react"
import Image from "next/image"
import Link from "next/link"
import { ArrowLeft, ShoppingCart, Plus, Minus } from "lucide-react"
import { use } from "react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { PriceHistoryChart } from "@/components/product-detail/price-history-chart"
import { CustomNavbar } from "@/components/custom-navbar"
import type { ProductData } from "@/lib/data/product-data"
import { CustomFooter } from "@/components/custom-footer"
import { SupermarketPriceTable } from "@/components/product-detail/supermarket-price-table"
import { Input } from "@/components/ui/input"
import { toast } from "@/hooks/use-toast"
import { API } from "@/lib/api/api"

export default function ProductPage({ params }: { params: { id: string } }) {
  const { id } = params
  const [product, setProduct] = useState<ProductData | null>(null)
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState(1)

  useEffect(() => {
    async function loadProduct() {
      try {
        setLoading(true)
        const productData = await API.getProductById(id)
        setProduct(productData)
      } catch (error) {
        console.error("Error loading product:", error)
      } finally {
        setLoading(false)
      }
    }

    loadProduct()
  }, [id])

  const addToCart = async () => {
    if (!product) return

    try {
      // Simulate API call to add to cart
      await API.addToCart(product.id, quantity)

      // Get existing cart from localStorage
      const savedCart = localStorage.getItem("priceTrackerCart")
      let cart = []

      if (savedCart) {
        try {
          cart = JSON.parse(savedCart)
          // Check if product already exists in cart
          const existingItemIndex = cart.findIndex((item: any) => item.productId === product.id)

          if (existingItemIndex >= 0) {
            // Update quantity if product already in cart
            cart[existingItemIndex].quantity += quantity
          } else {
            // Add new item to cart
            cart.push({ productId: product.id, quantity })
          }
        } catch (e) {
          console.error("Error parsing cart from localStorage", e)
          cart = [{ productId: product.id, quantity }]
        }
      } else {
        // Create new cart with this product
        cart = [{ productId: product.id, quantity }]
      }

      // Save updated cart to localStorage
      localStorage.setItem("priceTrackerCart", JSON.stringify(cart))

      // Show success message
      toast({
        title: "Added to cart",
        description: `${quantity} × ${product.name} added to your cart`,
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add product to cart",
        variant: "destructive",
      })
    }
  }

  const updateQuantity = (value: number) => {
    setQuantity(Math.max(1, value))
  }

  if (loading) {
    return (
      <div className="container flex items-center justify-center min-h-screen">
        <p>Loading...</p>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="container flex flex-col items-center justify-center min-h-screen gap-4">
        <h1 className="text-2xl font-bold">Product not found</h1>
        <p>We couldn't find the product you're looking for.</p>
        <Link href="/products">
          <Button>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Products
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <main className="flex min-h-screen flex-col bg-gray-50">
      <CustomNavbar />
      <div className="container flex-1 px-4 py-4 md:px-6">
        <Link
          href="/products"
          className="inline-flex items-center mb-3 text-sm font-medium text-gray-500 hover:text-gray-700"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to products
        </Link>

        {/* Product Title */}
        <div className="mb-3 flex justify-between items-center">
          <h1 className="text-2xl font-bold">{product.name}</h1>

          <div className="flex items-center gap-2">
            <div className="flex items-center border rounded-md">
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 rounded-r-none"
                onClick={() => updateQuantity(quantity - 1)}
              >
                <Minus className="h-4 w-4" />
              </Button>
              <Input
                type="number"
                value={quantity}
                onChange={(e) => updateQuantity(Number.parseInt(e.target.value) || 1)}
                className="h-8 w-16 text-center border-0 rounded-none"
                min="1"
              />
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 rounded-l-none"
                onClick={() => updateQuantity(quantity + 1)}
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            <Button onClick={addToCart} className="flex items-center gap-1">
              <ShoppingCart className="h-4 w-4" />
              Add to Cart
            </Button>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid gap-4">
          {/* Price History Chart - Full width */}
          <Card className="shadow-sm">
            <CardHeader className="pb-2 pt-4">
              <CardTitle className="text-xl">Price History</CardTitle>
            </CardHeader>
            <CardContent className="h-[300px] pt-0">
              <PriceHistoryChart data={product.priceHistory} />
            </CardContent>
          </Card>

          {/* Product Info and Current Prices - Two columns on desktop */}
          <div className="grid gap-4 md:grid-cols-2">
            {/* Product Info Card */}
            <Card className="shadow-sm">
              <CardHeader className="pb-2 pt-4">
                <CardTitle className="text-xl">Product Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 pt-0">
                <div className="flex justify-center p-3 bg-white rounded-lg border">
                  <Image
                    src={product.image || "/placeholder.svg"}
                    alt={product.name}
                    width={120}
                    height={120}
                    className="object-contain"
                  />
                </div>
                <div>
                  <h3 className="font-medium text-base">Name</h3>
                  <p className="text-base text-gray-500">{product.name}</p>
                </div>
                <div>
                  <h3 className="font-medium text-base">SKU</h3>
                  <p className="text-base text-gray-500">{product.sku}</p>
                </div>
                <div>
                  <h3 className="font-medium text-base">Description</h3>
                  <p className="text-base text-gray-500">{product.description}</p>
                </div>
              </CardContent>
            </Card>

            {/* Current Prices Card */}
            <Card className="shadow-sm">
              <CardHeader className="pb-2 pt-4">
                <CardTitle className="text-xl">Current Prices</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <SupermarketPriceTable prices={product.currentPrices} priceChanges={product.priceChanges} />
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
      <CustomFooter />
    </main>
  )
}