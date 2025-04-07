"use client"

import { Button } from "@/components/ui/button"
import { CartItem } from "./cart-item"
import type { ProductData } from "@/lib/data/product-data"

interface CartItemsListProps {
  cartItems: Array<{
    productId: string
    quantity: number
    product: ProductData
  }>
  selectedProducts: string[]
  onToggleSelect: (productId: string) => void
  onUpdateQuantity: (productId: string, quantity: number) => void
  onRemove: (productId: string) => void
  onSelectAll: () => void
  onDeselectAll: () => void
}

export function CartItemsList({
  cartItems,
  selectedProducts,
  onToggleSelect,
  onUpdateQuantity,
  onRemove,
  onSelectAll,
  onDeselectAll,
}: CartItemsListProps) {
  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <Button variant="outline" size="sm" onClick={onSelectAll} className="text-xs">
          Select All
        </Button>
        <Button variant="outline" size="sm" onClick={onDeselectAll} className="text-xs">
          Deselect All
        </Button>
      </div>

      <div className="space-y-2">
        {cartItems.map((item) => (
          <CartItem
            key={item.productId}
            productId={item.productId}
            quantity={item.quantity}
            product={item.product}
            isSelected={selectedProducts.includes(item.productId)}
            onToggleSelect={onToggleSelect}
            onUpdateQuantity={onUpdateQuantity}
            onRemove={onRemove}
          />
        ))}
      </div>
    </div>
  )
}

