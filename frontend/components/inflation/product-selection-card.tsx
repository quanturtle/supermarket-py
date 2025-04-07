"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Trash2 } from "lucide-react"
import type { ProductData } from "@/lib/data/product-data"

interface ProductSelectionCardProps {
  products: ProductData[]
  selectedProducts: string[]
  onToggleProduct: (productId: string) => void
}

export function ProductSelectionCard({ products, selectedProducts, onToggleProduct }: ProductSelectionCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Select Products</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="max-h-[400px] overflow-y-auto space-y-2 pr-2">
          {products.map((product) => (
            <div key={product.id} className="flex items-center space-x-2">
              <Checkbox
                id={`product-${product.id}`}
                checked={selectedProducts.includes(product.id)}
                onCheckedChange={() => onToggleProduct(product.id)}
              />
              <Label
                htmlFor={`product-${product.id}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {product.name}
              </Label>
            </div>
          ))}
        </div>

        <div className="pt-4 border-t">
          <h3 className="text-sm font-medium mb-2">Selected Products: {selectedProducts.length}</h3>
          <div className="flex flex-wrap gap-2">
            {selectedProducts.map((productId) => {
              const product = products.find((p) => p.id === productId)
              return product ? (
                <div
                  key={productId}
                  className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full flex items-center"
                >
                  <span className="mr-1">{product.name}</span>
                  <button onClick={() => onToggleProduct(productId)} className="text-gray-500 hover:text-gray-700">
                    <Trash2 className="h-3 w-3" />
                  </button>
                </div>
              ) : null
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

