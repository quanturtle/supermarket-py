import Link from "next/link"
import { SearchIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { mockProducts } from "@/lib/data/product-data"

export function CustomHero() {
  return (
    <section className="w-full py-12 md:py-24 lg:py-32">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Track Supermarket Prices</h1>
            <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl">
              Compare prices across 5 major supermarkets and view price history to make smarter shopping decisions.
            </p>
          </div>
          <div className="w-full max-w-md space-y-2">
            <form className="flex w-full max-w-md items-center space-x-2">
              <Input type="search" placeholder="Search for a product..." className="flex-1" />
              <Button type="submit">
                <SearchIcon className="h-4 w-4 mr-2" />
                Search
              </Button>
            </form>
            <p className="text-xs text-gray-500">Popular searches: Milk, Bread, Eggs, Bananas, Coffee</p>
          </div>
          <div className="flex flex-wrap justify-center gap-4 mt-8">
            <Link href="/products">
              <Button className="rounded-full">Browse All Products</Button>
            </Link>
            {["Milk", "Bread", "Eggs", "Bananas", "Coffee"].map((item) => {
              // Find the product ID by name
              const productId =
                Object.values(mockProducts).find((p) => p.name.toLowerCase().includes(item.toLowerCase()))?.id || "1"

              return (
                <Link href={`/product/${productId}`} key={item}>
                  <Button variant="outline" className="rounded-full">
                    {item}
                  </Button>
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}

