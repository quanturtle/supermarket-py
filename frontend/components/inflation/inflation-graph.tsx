import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import type { ProductInflation } from "@/lib/api/api"

interface InflationGraphProps {
  data: ProductInflation[]
}

export function InflationGraph({ data }: InflationGraphProps) {
  // Sort data by inflation rate in ascending order
  const chartData =
    data.length > 0
      ? [...data].sort((a, b) => a.inflation_rate - b.inflation_rate)
      : [
          { name: "Milk", sku: "MILK-1L-WHL", inflation_rate: 5.2 },
          { name: "Bread", sku: "BREAD-WHT-500G", inflation_rate: 7.8 },
          { name: "Eggs", sku: "EGGS-LRG-12CT", inflation_rate: 4.3 },
        ]

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>Per-Product Inflation</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 70 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={0} textAnchor="middle" height={70} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Inflation (%)", angle: -90, position: "insideLeft" }} tick={{ fontSize: 12 }} />
              <Tooltip
                formatter={(value) => [`${value.toFixed(2)}%`, "Inflation"]}
                labelFormatter={(label) => `Product: ${label}`}
              />
              <Bar
                dataKey="inflation_rate"
                name="Inflation Rate (%)"
                fill="#8884d8"
                label={{ position: "top", formatter: (value) => `${value.toFixed(2)}%` }}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
