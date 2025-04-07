"use client"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Minus, Plus, Trash2 } from "lucide-react"
import type { ProductData } from "@/lib/data/product-data"

interface CartItemProps {
  productId: string
  quantity: number
  product: ProductData
  isSelected: boolean
  onToggleSelect: (productId: string) => void
  onUpdateQuantity: (productId: string, quantity: number) => void
  onRemove: (productId: string) => void
}

export function CartItem({
  productId,
  quantity,
  product,
  isSelected,
  onToggleSelect,
  onUpdateQuantity,
  onRemove,
}: CartItemProps) {
  return (
    <div className="flex items-center border rounded-md p-3 mb-3">
      <div className="flex items-center justify-center mr-3">
        <Checkbox
          id={`product-${productId}`}
          checked={isSelected}
          onCheckedChange={() => onToggleSelect(productId)}
          className="h-5 w-5"
        />
      </div>

      <div className="flex-1">
        <Label htmlFor={`product-${productId}`} className="font-medium block mb-1">
          {product.name}
        </Label>
        <p className="text-sm text-gray-500">${product.lowestPrice.price.toFixed(2)} each</p>
      </div>

      <div className="flex items-center gap-1">
        <Button
          variant="outline"
          size="icon"
          className="h-8 w-8"
          onClick={() => onUpdateQuantity(productId, quantity - 1)}
        >
          <Minus className="h-3 w-3" />
        </Button>

        <div className="h-8 w-12 flex items-center justify-center border rounded text-sm">{quantity}</div>

        <Button
          variant="outline"
          size="icon"
          className="h-8 w-8"
          onClick={() => onUpdateQuantity(productId, quantity + 1)}
        >
          <Plus className="h-3 w-3" />
        </Button>

        <Button variant="ghost" size="icon" className="h-8 w-8 ml-1" onClick={() => onRemove(productId)}>
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

