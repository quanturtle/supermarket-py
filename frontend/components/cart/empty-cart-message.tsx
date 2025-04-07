"use client"

import { Button } from "@/components/ui/button"
import { ShoppingCart } from "lucide-react"

interface EmptyCartMessageProps {
    onCompare: () => void
    isDisabled: boolean
}

export function EmptyCartMessage({ onCompare, isDisabled }: EmptyCartMessageProps) {
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

