import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ExternalLink, ShoppingBag } from "lucide-react"
import type { ProductListResult, ProductFull, PriceComparisonResult } from "@/lib/api/api"
import Link from "next/link"
import { Button } from "@/components/ui/button"

type CartItem = {
  sku: string
  quantity: number
}

interface PriceComparisonGridProps {
  comparisons: PriceComparisonResult
  products: ProductListResult[]
  cart: CartItem[]
}

export function PriceComparisonGrid({ comparisons, products, cart }: PriceComparisonGridProps) {
  const { optimal, best, median, worst } = comparisons

  // Calculate total prices
  const calculateTotalPrice = (items: ProductFull[]) => {
    return items.reduce((total, item) => {
      const cartItem = cart.find((c) => c.sku === item.sku)
      const quantity = cartItem?.quantity || 1
      return total + item.price * quantity
    }, 0)
  }

  const optimalTotalPrice = calculateTotalPrice(optimal)
  const bestTotalPrice = calculateTotalPrice(best)
  const medianTotalPrice = calculateTotalPrice(median)
  const worstTotalPrice = calculateTotalPrice(worst)

  // Group optimal items by supermarket
  const optimalBySupermarket = optimal.reduce(
    (acc, item) => {
      const supermarketId = item.supermarket_id
      if (!acc[supermarketId]) {
        acc[supermarketId] = []
      }
      acc[supermarketId].push(item)
      return acc
    },
    {} as Record<number, ProductFull[]>,
  )

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Optimal Combination */}
        <Card className="border-purple-200 flex flex-col h-full">
          <CardHeader className="bg-purple-50 border-b border-purple-100 pb-3">
            <CardTitle className="text-purple-800 text-lg flex items-center justify-between">
              <span>Optimal Combination</span>
            </CardTitle>
            <CardDescription className="text-purple-700">Total: ${optimalTotalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 flex-1 overflow-auto">
            <div className="h-[300px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-xs">Product</TableHead>
                    <TableHead className="text-xs text-right">Price</TableHead>
                    <TableHead className="text-xs text-right">Total</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {optimal.map((item) => {
                    const product = products.find((p) => p.sku === item.sku)
                    const cartItem = cart.find((c) => c.sku === item.sku)
                    const quantity = cartItem?.quantity || 1
                    const total = item.price * quantity

                    return (
                      <TableRow key={item.sku}>
                        <TableCell className="py-1">
                          <div className="flex flex-col">
                            <span className="text-xs font-medium">{product?.name || item.name}</span>
                            <span className="text-xs text-gray-500">× {quantity}</span>
                          </div>
                        </TableCell>
                        <TableCell className="py-1 text-xs text-right">${item.price}</TableCell>
                        <TableCell className="py-1 text-xs text-right">${total}</TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
          <CardFooter className="pt-2 pb-3 border-t flex justify-center">
            <Link href="/cart/shopping-list">
              <Button variant="outline" size="sm" className="text-xs">
                <ShoppingBag className="h-3 w-3 mr-1" />
                View Shopping List
              </Button>
            </Link>
          </CardFooter>
        </Card>

        {/* Best Price Supermarket */}
        <Card className="border-green-200 flex flex-col h-full">
          <CardHeader className="bg-green-50 border-b border-green-100 pb-3">
            <CardTitle className="text-green-800 text-lg">Best: Supermarket {best[0]?.supermarket_id}</CardTitle>
            <CardDescription className="text-green-700">Total: ${bestTotalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 flex-1 overflow-auto">
            <div className="h-[300px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-xs">Product</TableHead>
                    <TableHead className="text-xs text-right">Price</TableHead>
                    <TableHead className="text-xs text-right">Total</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {best.map((item) => {
                    const product = products.find((p) => p.sku === item.sku)
                    const cartItem = cart.find((c) => c.sku === item.sku)
                    const quantity = cartItem?.quantity || 1
                    const total = item.price * quantity

                    return (
                      <TableRow key={item.sku}>
                        <TableCell className="py-1">
                          <div className="flex flex-col">
                            <span className="text-xs font-medium">{product?.name || item.name}</span>
                            <span className="text-xs text-gray-500">×{quantity}</span>
                          </div>
                        </TableCell>
                        <TableCell className="py-1 text-xs text-right">${item.price}</TableCell>
                        <TableCell className="py-1 text-xs text-right">${total}</TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
          <CardFooter className="pt-2 pb-3 border-t flex justify-center">
            <Link href={`/cart/shopping-list?supermarket=${best[0]?.supermarket_id}`}>
              <Button variant="outline" size="sm" className="text-xs">
                <ExternalLink className="h-3 w-3 mr-1" />
                Shop at Supermarket {best[0]?.supermarket_id}
              </Button>
            </Link>
          </CardFooter>
        </Card>

        {/* Median Price Supermarket */}
        <Card className="flex flex-col h-full">
          <CardHeader className="pb-3 border-b">
            <CardTitle className="text-lg">Median: Supermarket {median[0]?.supermarket_id}</CardTitle>
            <CardDescription>Total: ${medianTotalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 flex-1 overflow-auto">
            <div className="h-[300px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-xs">Product</TableHead>
                    <TableHead className="text-xs text-right">Price</TableHead>
                    <TableHead className="text-xs text-right">Total</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {median.map((item) => {
                    const product = products.find((p) => p.sku === item.sku)
                    const cartItem = cart.find((c) => c.sku === item.sku)
                    const quantity = cartItem?.quantity || 1
                    const total = item.price * quantity

                    return (
                      <TableRow key={item.sku}>
                        <TableCell className="py-1">
                          <div className="flex flex-col">
                            <span className="text-xs font-medium">{product?.name || item.name}</span>
                            <span className="text-xs text-gray-500">×{quantity}</span>
                          </div>
                        </TableCell>
                        <TableCell className="py-1 text-xs text-right">${item.price}</TableCell>
                        <TableCell className="py-1 text-xs text-right">${total}</TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
          <CardFooter className="pt-2 pb-3 border-t flex justify-center">
            <Link href={`/cart/shopping-list?supermarket=${median[0]?.supermarket_id}`}>
              <Button variant="outline" size="sm" className="text-xs">
                <ExternalLink className="h-3 w-3 mr-1" />
                Shop at Supermarket {median[0]?.supermarket_id}
              </Button>
            </Link>
          </CardFooter>
        </Card>

        {/* Worst Price Supermarket */}
        <Card className="border-red-200 flex flex-col h-full">
          <CardHeader className="bg-red-50 border-b border-red-100 pb-3">
            <CardTitle className="text-red-800 text-lg">Worst: Supermarket {worst[0]?.supermarket_id}</CardTitle>
            <CardDescription className="text-red-700">Total: ${worstTotalPrice.toFixed(2)}</CardDescription>
          </CardHeader>
          <CardContent className="pt-3 flex-1 overflow-auto">
            <div className="h-[300px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-xs">Product</TableHead>
                    <TableHead className="text-xs text-right">Price</TableHead>
                    <TableHead className="text-xs text-right">Total</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {worst.map((item) => {
                    const product = products.find((p) => p.sku === item.sku)
                    const cartItem = cart.find((c) => c.sku === item.sku)
                    const quantity = cartItem?.quantity || 1
                    const total = item.price * quantity

                    return (
                      <TableRow key={item.sku}>
                        <TableCell className="py-1">
                          <div className="flex flex-col">
                            <span className="text-xs font-medium">{product?.name || item.name}</span>
                            <span className="text-xs text-gray-500">×{quantity}</span>
                          </div>
                        </TableCell>
                        <TableCell className="py-1 text-xs text-right">${item.price}</TableCell>
                        <TableCell className="py-1 text-xs text-right">${total}</TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
          <CardFooter className="pt-2 pb-3 border-t flex justify-center">
            <Link href={`/cart/shopping-list?supermarket=${worst[0]?.supermarket_id}`}>
              <Button variant="outline" size="sm" className="text-xs">
                <ExternalLink className="h-3 w-3 mr-1" />
                Shop at Supermarket {worst[0]?.supermarket_id}
              </Button>
            </Link>
          </CardFooter>
        </Card>
      </div>

      <div className="p-3 bg-gray-50 rounded-md text-sm text-gray-700 border">
        <p>
          <strong>Savings Summary:</strong> Shopping at the best supermarket would save you $
          {(worstTotalPrice - bestTotalPrice).toFixed(2)} compared to the worst option. Using the optimal combination
          would save you an additional ${(bestTotalPrice - optimalTotalPrice).toFixed(2)}.
        </p>
      </div>
    </div>
  )
}
