"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import Image from "next/image"
import type { ProductData } from "@/lib/data/product-data"
import { Card, CardContent } from "@/components/ui/card"
import { API } from "@/lib/api/api"

export default function ProductsPage() {
    const [products, setProducts] = useState<ProductData[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadProducts() {
            try {
                setLoading(true)
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

    if (loading) {
        return (
            <div className="container flex items-center justify-center min-h-screen">
                <p>Loading products...</p>
            </div>
        )
    }

    // Group products by first letter - moved here after loading check
    const groupedProducts: Record<string, ProductData[]> = {}

    products.forEach((product) => {
        const firstLetter = product.name.charAt(0).toUpperCase()
        if (!groupedProducts[firstLetter]) {
            groupedProducts[firstLetter] = []
        }
        groupedProducts[firstLetter].push(product)
    })

    // Get sorted letters
    const letters = Object.keys(groupedProducts).sort()

    return (
        <>
            <h1 className="text-3xl font-bold mb-6">All Products</h1>

            <div className="space-y-8">
                {letters.map((letter) => (
                    <div key={letter} className="space-y-4">
                        <h2 className="text-2xl font-bold border-b border-gray-200 pb-2">{letter}</h2>
                        <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                            {groupedProducts[letter].map((product) => (
                                <Link href={`/product/${product.id}`} key={product.id}>
                                    <Card className="h-full hover:shadow-md transition-shadow">
                                        <CardContent className="p-4 flex flex-col h-full">
                                            <div className="flex justify-center mb-3">
                                                <Image
                                                    src={product.image || "/placeholder.svg"}
                                                    alt={product.name}
                                                    width={80}
                                                    height={80}
                                                    className="object-contain"
                                                />
                                            </div>
                                            <h3 className="font-medium text-base mb-1">{product.name}</h3>
                                            <p className="text-sm text-gray-500 mb-2 line-clamp-2">{product.description}</p>
                                            <div className="mt-auto flex justify-between items-center">
                                                <span className="text-sm text-gray-500">SKU: {product.sku}</span>
                                                <span className="font-bold text-sm">${product.lowestPrice.price.toFixed(2)}</span>
                                            </div>
                                        </CardContent>
                                    </Card>
                                </Link>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}