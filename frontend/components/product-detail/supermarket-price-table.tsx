import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ArrowDown, ArrowUp, Minus } from "lucide-react"
import type { PriceChange } from "@/lib/api/api"

interface SupermarketPriceTableProps {
  priceChanges: PriceChange[]
}

export function SupermarketPriceTable({ priceChanges }: SupermarketPriceTableProps) {
  if (!priceChanges || priceChanges.length === 0) {
    return <div className="text-center py-4">No price data available</div>
  }

  // Sort prices from lowest to highest
  const sortedPrices = [...priceChanges].sort((a, b) => a.price - b.price)

  return (
    <Table>
      <TableHeader>
        <TableRow className="border-b border-gray-200">
          <TableHead className="font-medium py-2 text-base">Supermarket</TableHead>
          <TableHead className="text-right font-medium py-2 text-base">Price</TableHead>
          <TableHead className="text-right font-medium py-2 text-base w-24">Change</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {sortedPrices.map((priceChange, index) => {
          const supermarket = `Supermarket ${priceChange.supermarket_id}`
          const price = priceChange.price
          const pctChange = priceChange.pct_change

          // Determine change styling
          const changeColor = pctChange === 0 ? "text-gray-400" : pctChange < 0 ? "text-green-500" : "text-red-500"

          // Format change value
          const changeValue = pctChange === 0 ? "0.00%" : `${Math.abs(pctChange)}%`

          // Determine icon
          const ChangeIcon = pctChange === 0 ? Minus : pctChange < 0 ? ArrowDown : ArrowUp

          return (
            <TableRow key={supermarket} className={index < sortedPrices.length - 1 ? "border-b border-gray-100" : ""}>
              <TableCell className="py-3 font-medium">
                {supermarket}
                {index === 0 && (
                  <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">Best Price</span>
                )}
              </TableCell>
              <TableCell className="py-3 text-right font-bold">${price}</TableCell>
              <TableCell className={`py-3 text-right ${changeColor}`}>
                <div className="flex items-center justify-end gap-1">
                  <ChangeIcon className="h-3.5 w-3.5" />
                  <span>{changeValue}</span>
                </div>
              </TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )
}
