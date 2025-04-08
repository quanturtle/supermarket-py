"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Minus, Package, Plus, Search } from "lucide-react"
import Image from "next/image"
import type { ProductData } from "@/lib/data/product-data"
import { useCart } from "@/hooks/use-cart"
import { API } from "@/lib/api/api"

export function SearchProductDialog() {
    const [products, setProducts] = useState<ProductData[]>([])
    const [searchQuery, setSearchQuery] = useState("")
    const [searchResults, setSearchResults] = useState<ProductData[]>([])
    const [quantities, setQuantities] = useState<Record<string, number>>({})
    const [isOpen, setIsOpen] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const { addToCart } = useCart()

    useEffect(() => {
        async function loadProducts() {
            try {
                const allProducts = await API.getAllProducts()
                setProducts(allProducts)
            } catch (error) {
                console.error("Error loading products:", error)
            }
        }

        loadProducts()
    }, [])

    useEffect(() => {
        async function performSearch() {
            if (searchQuery.trim() === "") {
                setSearchResults([])
                return
            }

            setIsLoading(true)
            try {
                const results = await API.searchProducts(searchQuery)
                setSearchResults(results)
            } catch (error) {
                console.error("Error searching products:", error)
            } finally {
                setIsLoading(false)
            }
        }

        // Debounce search
        const timer = setTimeout(() => {
            performSearch()
        }, 300)

        return () => clearTimeout(timer)
    }, [searchQuery])

    const handleQuantityChange = (productId: string, value: number) => {
        setQuantities((prev) => ({
            ...prev,
            [productId]: Math.max(1, value),
        }))
    }

    const getProductQuantity = (productId: string) => {
        return quantities[productId] || 1
    }

    const handleAddToCart = async (productId: string, quantity: number) => {
        try {
            await API.addToCart(productId, quantity)
            addToCart(productId, quantity)
            // Reset quantity after adding
            setQuantities((prev) => ({ ...prev, [productId]: 1 }))
        } catch (error) {
            console.error("Error adding to cart:", error)
        }
    }

    return (
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
                <Button variant="outline" className="w-full sm:w-auto">
                    <Search className="h-4 w-4 mr-2" />
                    Search & Add Products
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
                <DialogHeader>
                    <DialogTitle>Search Products</DialogTitle>
                    <DialogDescription>Search for products to add to your comparison cart</DialogDescription>
                </DialogHeader>

                <div className="mt-4 space-y-4">
                    <div className="flex gap-2">
                        <Input
                            placeholder="Search products..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="flex-1"
                        />
                    </div>

                    <ScrollArea className="h-[300px] rounded-md border p-2">
                        {isLoading ? (
                            <div className="text-center py-8 text-gray-500">Searching...</div>
                        ) : searchResults.length > 0 ? (
                            <div className="space-y-4">
                                {searchResults.map((product) => (
                                    <div key={product.id} className="flex items-center justify-between border-b pb-3">
                                        <div className="flex items-center gap-3">
                                            <div className="h-12 w-12 relative">
                                                <Image
                                                    src={product.image || "/placeholder.svg"}
                                                    alt={product.name}
                                                    fill
                                                    className="object-contain"
                                                />
                                            </div>
                                            <div>
                                                <h3 className="font-medium">{product.name}</h3>
                                                <p className="text-xs text-gray-500">
                                                    ${product.lowestPrice.price.toFixed(2)} at {product.lowestPrice.store}
                                                </p>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-2">
                                            <div className="flex items-center">
                                                <Button
                                                    variant="outline"
                                                    size="icon"
                                                    className="h-8 w-8 rounded-r-none"
                                                    onClick={() => handleQuantityChange(product.id, getProductQuantity(product.id) - 1)}
                                                >
                                                    <Minus className="h-3 w-3" />
                                                </Button>
                                                <div className="h-8 w-12 text-center rounded-none border flex items-center justify-center bg-white">
                                                    {getProductQuantity(product.id)}
                                                </div>
                                                <Button
                                                    variant="outline"
                                                    size="icon"
                                                    className="h-8 w-8 rounded-l-none"
                                                    onClick={() => handleQuantityChange(product.id, getProductQuantity(product.id) + 1)}
                                                >
                                                    <Plus className="h-3 w-3" />
                                                </Button>
                                            </div>

                                            <Button
                                                size="sm"
                                                onClick={() => {
                                                    handleAddToCart(product.id, getProductQuantity(product.id))
                                                    setIsOpen(false)
                                                }}
                                            >
                                                Add
                                            </Button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : searchQuery.trim() !== "" ? (
                            <div className="text-center py-8 text-gray-500">No products found matching "{searchQuery}"</div>
                        ) : (
                            <div className="text-center py-8 text-gray-500">
                                <Package className="h-12 w-12 mx-auto mb-2 opacity-30" />
                                <p>Type to search for products</p>
                            </div>
                        )}
                    </ScrollArea>
                </div>
            </DialogContent>
        </Dialog>
    )
}