"use client"

import { useEffect, useState, use } from "react"
import Link from "next/link"
import { ArrowLeft, ShoppingCart, Plus, Minus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { PriceHistoryChart } from "@/components/product-detail/price-history-chart"
import { SupermarketPriceTable } from "@/components/product-detail/supermarket-price-table"
import { ProductInfoCard } from "@/components/product-detail/product-info-card"
import { Input } from "@/components/ui/input"
import { API, type ProductDetailResult } from "@/lib/api/api"
import { useCart } from "@/hooks/use-cart"

export default function ProductPage({ params }: { params: { sku: string } }) {
    // Unwrap params using React.use()
    // const unwrappedParams = use(params)
    const { sku } = params;

    const { addToCart } = useCart()

    const [product, setProduct] = useState<ProductDetailResult | null>(null)
    const [loading, setLoading] = useState(true)
    const [quantity, setQuantity] = useState(1)

    useEffect(() => {
        async function loadProduct() {
            try {
                setLoading(true)
                // Get the detailed product info by SKU
                const productDetail = await API.getProductBySKU(sku)
                setProduct(productDetail)
            } catch (error) {
                console.error("Error loading product:", error)
            } finally {
                setLoading(false)
            }
        }

        loadProduct()
    }, [sku])

    const handleAddToCart = () => {
        if (!product) return
        // Add to cart using the useCart hook (which handles localStorage)
        addToCart(product.product_info.sku, quantity)
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
                <Link href="/catalog">
                    <Button>
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Catalog
                    </Button>
                </Link>
            </div>
        )
    }

    return (
        <>
            <Link
                href="/catalog"
                className="inline-flex items-center mb-3 text-sm font-medium text-gray-500 hover:text-gray-700"
            >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to catalog
            </Link>

            {/* Product Title */}
            <div className="mb-3 flex justify-between items-center">
                <h1 className="text-2xl font-bold">{product.product_info.name}</h1>

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

                    <Button onClick={handleAddToCart} className="flex items-center gap-1">
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
                        <PriceHistoryChart history={product.history} />
                    </CardContent>
                </Card>

                {/* Product Info and Current Prices - Two columns on desktop */}
                <div className="grid gap-4 md:grid-cols-2">
                    {/* Product Info Card */}
                    <ProductInfoCard productInfo={product.product_info} sku={product.product_info.sku} />

                    {/* Current Prices Card */}
                    <Card className="shadow-sm">
                        <CardHeader className="pb-2 pt-4">
                            <CardTitle className="text-xl">Current Prices</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                            <SupermarketPriceTable priceChanges={product.price_changes} />
                        </CardContent>
                    </Card>
                </div>
            </div>
        </>
    )
}
