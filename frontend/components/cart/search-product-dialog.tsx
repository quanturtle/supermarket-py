"use client"

import { useState, useEffect } from "react"
import { MagnifyingGlassIcon } from "@radix-ui/react-icons"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem } from "@/components/ui/command"
import { ScrollArea } from "@/components/ui/scroll-area"
import { API, type ProductListResult } from "@/lib/api/api"
import { useCart } from "@/hooks/use-cart"

export function SearchProductDialog() {
  const [open, setOpen] = useState(false)
  const [products, setProducts] = useState<ProductListResult[]>([])
  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const { addToCart } = useCart()

  useEffect(() => {
    const loadProducts = async () => {
      setLoading(true)
      try {
        const results = await API.searchProducts(query)
        setProducts(results)
      } catch (error) {
        console.error("Error searching products:", error)
        setProducts([])
      } finally {
        setLoading(false)
      }
    }

    if (query) {
      loadProducts()
    } else {
      setProducts([])
    }
  }, [query])

  const handleAddToCart = (sku: string) => {
    addToCart(sku)
    setOpen(false) // Close the dialog after adding to cart
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="w-full">
          <MagnifyingGlassIcon className="mr-2 h-4 w-4" />
          Search Products
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Search Products</DialogTitle>
          <DialogDescription>Search for products to add to your cart for price comparison.</DialogDescription>
        </DialogHeader>
        <Command>
          <CommandInput placeholder="Type a product name..." value={query} onValueChange={setQuery} />
          <CommandEmpty>{loading ? "Loading..." : "No products found."}</CommandEmpty>
          <ScrollArea className="h-[300px]">
            <CommandGroup>
              {products.map((product) => (
                <CommandItem key={product.sku} onSelect={() => handleAddToCart(product.sku)}>
                  {product.name}
                </CommandItem>
              ))}
            </CommandGroup>
          </ScrollArea>
        </Command>
      </DialogContent>
    </Dialog>
  )
}
