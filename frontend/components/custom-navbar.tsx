"use client"

import Link from "next/link"
import { ShoppingCart, LineChart, Package } from "lucide-react"
import { useCart } from "@/hooks/use-cart"

export function CustomNavbar() {
  const { cart } = useCart()

  // Count unique products (SKUs) in cart
  const uniqueProductCount = cart.length

  return (
    <header className="sticky top-0 z-10 bg-white border-b">
      <div className="container flex h-16 items-center px-4 md:px-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl font-bold">PriceTracker</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6 items-center">
          <Link
            href="/catalog"
            className="text-sm font-medium hover:underline underline-offset-4 flex items-center gap-1"
          >
            <Package className="h-4 w-4" />
            <span className="hidden sm:inline">Catalog</span>
          </Link>
          <Link
            href="/inflation-calculator"
            className="text-sm font-medium hover:underline underline-offset-4 flex items-center gap-1"
          >
            <LineChart className="h-4 w-4" />
            <span className="hidden sm:inline">Inflation Calculator</span>
          </Link>
          <Link
            href="/cart"
            className="text-sm font-medium hover:underline underline-offset-4 flex items-center gap-1 relative"
          >
            <ShoppingCart className="h-4 w-4" />
            <span className="hidden sm:inline">Compare Carts</span>
            {uniqueProductCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {uniqueProductCount}
              </span>
            )}
          </Link>
          <Link href="/about" className="text-sm font-medium hover:underline underline-offset-4">
            <span className="hidden sm:inline">About</span>
          </Link>
          <Link href="/contact" className="text-sm font-medium hover:underline underline-offset-4">
            <span className="hidden sm:inline">Contact</span>
          </Link>
        </nav>
      </div>
    </header>
  )
}
