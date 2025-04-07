import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

interface ProductInflationChartProps {
  data: Array<{
    name: string
    percentageChange: string
    [key: string]: any
  }>
}

export function ProductInflationChart({ data }: ProductInflationChartProps) {
  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>Per-Product Inflation</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 70 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={0} textAnchor="middle" height={70} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Inflation (%)", angle: -90, position: "insideLeft" }} tick={{ fontSize: 12 }} />
              <Tooltip
                formatter={(value) => [`${value}%`, "Inflation"]}
                labelFormatter={(label) => `Product: ${label}`}
              />
              <Bar
                dataKey="percentageChange"
                name="Inflation Rate (%)"
                fill="#8884d8"
                label={{ position: "top", formatter: (value) => `${value}%` }}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}

