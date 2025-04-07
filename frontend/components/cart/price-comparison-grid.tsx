import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ExternalLink, ShoppingBag } from "lucide-react"
import type { ProductData } from "@/lib/data/product-data"
import Link from "next/link"
import { Button } from "@/components/ui/button"

type CartItem = {
  productId: string
  quantity: number
}

type SupermarketPricing = {
  name: string
  totalPrice: number
  items: {
    productId: string
    price: number
    total: number
  }[]
}

type OptimalCombination = {
  totalPrice: number
  items: {
    productId: string
    supermarket: string
    price: number
    total: number
  }[]
}

interface PriceComparisonGridProps {
  comparisons: {
    worst: SupermarketPricing
    average: SupermarketPricing
    best: SupermarketPricing
    optimal: OptimalCombination
  }
  products: ProductData[]
  cart: CartItem[]
}

export function PriceComparisonGrid({ comparisons, products, cart }: PriceComparisonGridProps) {
  const { worst, average, best, optimal } = comparisons

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Optimal Combination */}
        <Card className="border-purple-200">
          <CardHeader className="bg-purple-50 border-b border-purple-100 pb-3">
            <CardTitle className="text-purple-800 text-lg flex items-center justify-between">
              <span>Optimal Combination</span>
              <Link href="/cart/shopping-list">
                <ShoppingBag className="h-5 w-5 text-purple-700 cursor-pointer hover:text-purple-900" />
              </Link>
            </CardTitle>
            <CardDescription className="text-purple-700">Total: ${optimal.totalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 h-[300px] overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs">Product</TableHead>
                  <TableHead className="text-xs">Price</TableHead>
                  <TableHead className="text-xs">Total</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {optimal.items.map((item) => {
                  const product = products.find((p) => p.id === item.productId)
                  const cartItem = cart.find((c) => c.productId === item.productId)
                  return (
                    <TableRow key={item.productId}>
                      <TableCell className="py-1">
                        <div className="flex items-center gap-1">
                          <span className="text-xs">{product?.name}</span>
                          <span className="text-xs text-gray-500">×{cartItem?.quantity}</span>
                        </div>
                      </TableCell>
                      <TableCell className="py-1 text-xs">${item.price.toFixed(2)}</TableCell>
                      <TableCell className="py-1 text-xs">${item.total.toFixed(2)}</TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
            <div className="mt-3 text-center">
              <Link href="/cart/shopping-list">
                <Button variant="outline" size="sm" className="text-xs">
                  <ShoppingBag className="h-3 w-3 mr-1" />
                  View Shopping List
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Best Price Supermarket */}
        <Card className="border-green-200">
          <CardHeader className="bg-green-50 border-b border-green-100 pb-3">
            <CardTitle className="text-green-800 text-lg">Best: {best.name}</CardTitle>
            <CardDescription className="text-green-700">Total: ${best.totalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 h-[300px] overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs">Product</TableHead>
                  <TableHead className="text-xs">Price</TableHead>
                  <TableHead className="text-xs">Total</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {best.items.map((item) => {
                  const product = products.find((p) => p.id === item.productId)
                  const cartItem = cart.find((c) => c.productId === item.productId)
                  return (
                    <TableRow key={item.productId}>
                      <TableCell className="py-1">
                        <div className="flex items-center gap-1">
                          <span className="text-xs">{product?.name}</span>
                          <span className="text-xs text-gray-500">×{cartItem?.quantity}</span>
                        </div>
                      </TableCell>
                      <TableCell className="py-1 text-xs">${item.price.toFixed(2)}</TableCell>
                      <TableCell className="py-1 text-xs">${item.total.toFixed(2)}</TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
            <div className="mt-3 text-center">
              <Link href={`/cart/shopping-list?supermarket=${encodeURIComponent(best.name)}`}>
                <Button variant="outline" size="sm" className="text-xs">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  Shop at {best.name}
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Average Price Supermarket */}
        <Card>
          <CardHeader className="pb-3 border-b border-black-100">
            <CardTitle className="text-lg">Average: {average.name}</CardTitle>
            <CardDescription>Total: ${average.totalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 h-[300px] overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs">Product</TableHead>
                  <TableHead className="text-xs">Price</TableHead>
                  <TableHead className="text-xs">Total</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {average.items.map((item) => {
                  const product = products.find((p) => p.id === item.productId)
                  const cartItem = cart.find((c) => c.productId === item.productId)
                  return (
                    <TableRow key={item.productId}>
                      <TableCell className="py-1">
                        <div className="flex items-center gap-1">
                          <span className="text-xs">{product?.name}</span>
                          <span className="text-xs text-gray-500">×{cartItem?.quantity}</span>
                        </div>
                      </TableCell>
                      <TableCell className="py-1 text-xs">${item.price.toFixed(2)}</TableCell>
                      <TableCell className="py-1 text-xs">${item.total.toFixed(2)}</TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
            <div className="mt-3 text-center">
              <Link href={`/cart/shopping-list?supermarket=${encodeURIComponent(average.name)}`}>
                <Button variant="outline" size="sm" className="text-xs">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  Shop at {average.name}
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Worst Price Supermarket */}
        <Card className="border-red-200">
          <CardHeader className="bg-red-50 border-b border-red-100 pb-3">
            <CardTitle className="text-red-800 text-lg">Worst: {worst.name}</CardTitle>
            <CardDescription className="text-red-700">Total: ${worst.totalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 h-[300px] overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs">Product</TableHead>
                  <TableHead className="text-xs">Price</TableHead>
                  <TableHead className="text-xs">Total</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {worst.items.map((item) => {
                  const product = products.find((p) => p.id === item.productId)
                  const cartItem = cart.find((c) => c.productId === item.productId)
                  return (
                    <TableRow key={item.productId}>
                      <TableCell className="py-1">
                        <div className="flex items-center gap-1">
                          <span className="text-xs">{product?.name}</span>
                          <span className="text-xs text-gray-500">×{cartItem?.quantity}</span>
                        </div>
                      </TableCell>
                      <TableCell className="py-1 text-xs">${item.price.toFixed(2)}</TableCell>
                      <TableCell className="py-1 text-xs">${item.total.toFixed(2)}</TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
            <div className="mt-3 text-center">
              <Link href={`/cart/shopping-list?supermarket=${encodeURIComponent(worst.name)}`}>
                <Button variant="outline" size="sm" className="text-xs">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  Shop at {worst.name}
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="p-3 bg-gray-50 rounded-md text-sm text-gray-700 border">
        <p>
          <strong>Savings Summary:</strong> Shopping at the best supermarket ({best.name}) would save you $
          {(worst.totalPrice - best.totalPrice).toFixed(2)} compared to the worst option. Using the optimal combination would save you an additional $
          {(best.totalPrice - optimal.totalPrice).toFixed(2)}.
        </p>
      </div>
    </div>
  )
}