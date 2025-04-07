import Link from "next/link"
import { ShoppingCart, LineChart, Package } from "lucide-react"

export function CustomNavbar() {
  return (
    <header className="sticky top-0 z-10 bg-white border-b">
      <div className="container flex h-16 items-center px-4 md:px-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl font-bold">PriceTracker</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6 items-center">
          <Link
            href="/products"
            className="text-sm font-medium hover:underline underline-offset-4 flex items-center gap-1"
          >
            <Package className="h-4 w-4" />
            <span>Products</span>
          </Link>
          <Link
            href="/inflation-calculator"
            className="text-sm font-medium hover:underline underline-offset-4 flex items-center gap-1"
          >
            <LineChart className="h-4 w-4" />
            <span>Inflation Calculator</span>
          </Link>
          <Link href="/cart" className="text-sm font-medium hover:underline underline-offset-4 flex items-center gap-1">
            <ShoppingCart className="h-4 w-4" />
            <span>Compare Carts</span>
          </Link>
          <Link href="/about" className="text-sm font-medium hover:underline underline-offset-4">
            <span>About</span>
          </Link>
          <Link href="/contact" className="text-sm font-medium hover:underline underline-offset-4">
            <span>Contact</span>
          </Link>
        </nav>
      </div>
    </header>
  )
}

