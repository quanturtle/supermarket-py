"use client"

import { Button } from "@/components/ui/button"
import { SearchProductDialog } from "./search-product-dialog"

interface CartHeaderProps {
  cartItemsCount: number
  onClearCart: () => void
  onCompareCartPrices: () => void
  isCompareDisabled: boolean
}

export function CartHeader({ cartItemsCount, onClearCart, onCompareCartPrices, isCompareDisabled }: CartHeaderProps) {
  return (
    <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-6 gap-4">
      <h1 className="text-3xl font-bold">Compare Prices</h1>

      <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
        <div className="relative flex-1">
          <SearchProductDialog />
        </div>

        <Button variant="outline" onClick={onClearCart} disabled={cartItemsCount === 0}>
          Clear Cart
        </Button>

        <Button onClick={onCompareCartPrices} disabled={isCompareDisabled}>
          Compare Prices
        </Button>
      </div>
    </div>
  )
}

