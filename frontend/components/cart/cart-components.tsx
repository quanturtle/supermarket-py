"use client"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Minus, Plus, Trash2, ShoppingCart } from "lucide-react"
import { SearchProductDialog } from "./search-product-dialog"
import type { ProductListResult, PriceComparisonResult } from "@/lib/api/api"
import { PriceComparisonGrid } from "./price-comparison-grid"

// CartHeader Component
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

// CartItem Component
interface CartItemProps {
  sku: string
  quantity: number
  product: ProductListResult
  isSelected: boolean
  onToggleSelect: (sku: string) => void
  onUpdateQuantity: (sku: string, quantity: number) => void
  onRemove: (sku: string) => void
}

function CartItem({ sku, quantity, product, isSelected, onToggleSelect, onUpdateQuantity, onRemove }: CartItemProps) {
  return (
    <div className="flex items-center border rounded-md p-3 mb-3">
      <div className="flex items-center justify-center mr-3">
        <Checkbox
          id={`product-${sku}`}
          checked={isSelected}
          onCheckedChange={() => onToggleSelect(sku)}
          className="h-5 w-5"
        />
      </div>

      <div className="flex-1">
        <Label htmlFor={`product-${sku}`} className="font-medium block mb-1">
          {product.name}
        </Label>
        <p className="text-sm text-gray-500">SKU: {product.sku}</p>
      </div>

      <div className="flex items-center gap-1">
        <Button variant="outline" size="icon" className="h-8 w-8" onClick={() => onUpdateQuantity(sku, quantity - 1)}>
          <Minus className="h-3 w-3" />
        </Button>

        <div className="h-8 w-12 flex items-center justify-center border rounded text-sm">{quantity}</div>

        <Button variant="outline" size="icon" className="h-8 w-8" onClick={() => onUpdateQuantity(sku, quantity + 1)}>
          <Plus className="h-3 w-3" />
        </Button>

        <Button variant="ghost" size="icon" className="h-8 w-8 ml-1" onClick={() => onRemove(sku)}>
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

// CartItemsList Component
interface CartItemsListProps {
  cartItems: Array<{
    sku: string
    quantity: number
    product: ProductListResult
  }>
  selectedProducts: string[]
  onToggleSelect: (sku: string) => void
  onUpdateQuantity: (sku: string, quantity: number) => void
  onRemove: (sku: string) => void
  onSelectAll: () => void
  onDeselectAll: () => void
}

function CartItemsList({
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
            key={item.sku}
            sku={item.sku}
            quantity={item.quantity}
            product={item.product}
            isSelected={selectedProducts.includes(item.sku)}
            onToggleSelect={onToggleSelect}
            onUpdateQuantity={onUpdateQuantity}
            onRemove={onRemove}
          />
        ))}
      </div>
    </div>
  )
}

// EmptyCartMessage Component
interface EmptyCartMessageProps {
  onCompare: () => void
  isDisabled: boolean
}

function EmptyCartMessage({ onCompare, isDisabled }: EmptyCartMessageProps) {
  return (
    <div className="text-center py-8">
      <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <h2 className="text-lg font-semibold mb-2">Your cart is empty</h2>
      <p className="text-gray-500 max-w-md mx-auto mb-6">
        Search for products to add them to your cart for price comparison.
      </p>
      {!isDisabled && <Button onClick={onCompare}>Compare Prices</Button>}
    </div>
  )
}

// CartCard Component
interface CartCardProps {
  cartItems: Array<{
    sku: string
    quantity: number
    product: ProductListResult
  }>
  selectedProducts: string[]
  onToggleSelect: (sku: string) => void
  onUpdateQuantity: (sku: string, quantity: number) => void
  onRemove: (sku: string) => void
  onSelectAll: () => void
  onDeselectAll: () => void
  onCompare: () => void
  isCompareDisabled: boolean
}

export function CartCard({
  cartItems,
  selectedProducts,
  onToggleSelect,
  onUpdateQuantity,
  onRemove,
  onSelectAll,
  onDeselectAll,
  onCompare,
  isCompareDisabled,
}: CartCardProps) {
  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Your Cart ({cartItems.length})</CardTitle>
        <CardDescription>Select which items to include in your comparison</CardDescription>
      </CardHeader>
      <CardContent>
        {cartItems.length === 0 ? (
          <EmptyCartMessage onCompare={onCompare} isDisabled={isCompareDisabled} />
        ) : (
          <CartItemsList
            cartItems={cartItems}
            selectedProducts={selectedProducts}
            onToggleSelect={onToggleSelect}
            onUpdateQuantity={onUpdateQuantity}
            onRemove={onRemove}
            onSelectAll={onSelectAll}
            onDeselectAll={onDeselectAll}
          />
        )}
      </CardContent>
    </Card>
  )
}

// CartComparisonCard Component
type CartItem = {
  sku: string
  quantity: number
}

interface CartComparisonCardProps {
  comparing: boolean
  comparisonResults: PriceComparisonResult | null
  products: ProductListResult[]
  cart: CartItem[]
  onCompare: () => void
  isCompareDisabled: boolean
}

export function CartComparisonCard({
  comparing,
  comparisonResults,
  products,
  cart,
  onCompare,
  isCompareDisabled,
}: CartComparisonCardProps) {
  if (comparing) {
    return (
      <Card className="h-full flex items-center justify-center">
        <CardContent className="py-12 text-center">
          <div className="animate-pulse">
            <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Comparing Prices...</h2>
            <p className="text-gray-500 max-w-md mx-auto">We're calculating the best deals across all supermarkets.</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (comparisonResults) {
    return <PriceComparisonGrid comparisons={comparisonResults} products={products} cart={cart} />
  }

  return (
    <Card className="h-full flex items-center justify-center">
      <CardContent className="py-12 text-center">
        <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold mb-2">Ready to Compare</h2>
        <p className="text-gray-500 max-w-md mx-auto mb-6">
          Add products to your cart using the search button above, then click "Compare Prices" to see which supermarket
          offers the best deals.
        </p>
        <Button onClick={onCompare} disabled={isCompareDisabled}>
          Compare Prices
        </Button>
      </CardContent>
    </Card>
  )
}
