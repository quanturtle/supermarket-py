import Image from "next/image"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { ProductInfo } from "@/lib/api/api"

interface ProductInfoCardProps {
  productInfo: ProductInfo
  sku: string
}

export function ProductInfoCard({ productInfo, sku }: ProductInfoCardProps) {
  return (
    <Card className="shadow-sm">
      <CardHeader className="pb-2 pt-4">
        <CardTitle className="text-xl">Product Information</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 pt-0">
        <div className="flex justify-center p-3 bg-white rounded-lg border">
          <Image src={"/placeholder.svg"} alt={productInfo.name} width={120} height={120} className="object-contain" />
        </div>
        <div>
          <h3 className="font-medium text-base">Name</h3>
          <p className="text-base text-gray-500">{productInfo.name}</p>
        </div>
        <div>
          <h3 className="font-medium text-base">SKU</h3>
          <p className="text-base text-gray-500">{sku}</p>
        </div>
        <div>
          <h3 className="font-medium text-base">Description</h3>
          <p className="text-base text-gray-500">{productInfo.name}</p>
        </div>
      </CardContent>
    </Card>
  )
}
