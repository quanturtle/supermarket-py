import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ArrowDown, ArrowUp, Minus } from "lucide-react"

interface SupermarketPriceTableProps {
    prices: {
        [key: string]: number
    }
    priceChanges?: {
        [key: string]: number
    }
}

export function SupermarketPriceTable({ prices, priceChanges }: SupermarketPriceTableProps) {
    // Sort prices from lowest to highest
    const sortedPrices = Object.entries(prices).sort((a, b) => a[1] - b[1])

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
                {sortedPrices.map(([supermarket, price], index) => {
                    const priceChange = priceChanges ? priceChanges[supermarket] : 0

                    // Determine change styling
                    const changeColor = priceChange === 0 ? "text-gray-400" : priceChange < 0 ? "text-green-500" : "text-red-500"

                    // Format change value
                    const changeValue = priceChange === 0 ? "$0.00" : `$${Math.abs(priceChange).toFixed(2)}`

                    // Determine icon
                    const ChangeIcon = priceChange === 0 ? Minus : priceChange < 0 ? ArrowDown : ArrowUp

                    return (
                        <TableRow key={supermarket} className={index < sortedPrices.length - 1 ? "border-b border-gray-100" : ""}>
                            <TableCell className="py-3 font-medium">
                                {supermarket}
                                {index === 0 && (
                                    <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">Best Price</span>
                                )}
                            </TableCell>
                            <TableCell className="py-3 text-right font-bold">${price.toFixed(2)}</TableCell>
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

