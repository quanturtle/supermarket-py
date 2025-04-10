"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import type { ProductHistoryEntry } from "@/lib/api/api"

interface PriceHistoryChartProps {
  history: ProductHistoryEntry[]
}

export function PriceHistoryChart({ history }: PriceHistoryChartProps) {
  if (!history || history.length === 0) {
    return <div className="w-full h-full flex items-center justify-center">No price history data available</div>
  }

  // Group by exact date (yyyy-mm-dd)
  const groupedByDate = history.reduce(
    (acc, entry) => {
      const date = new Date(entry.created_at)
      // Format date as yyyy-mm-dd
      const dateKey = date.toISOString().split("T")[0]

      if (!acc[dateKey]) {
        acc[dateKey] = {}
      }

      // Use supermarket ID as the key
      const supermarketKey = `Supermarket ${entry.supermarket_id}`
      acc[dateKey][supermarketKey] = entry.price

      return acc
    },
    {} as Record<string, Record<string, number>>,
  )

  // Convert to array format for chart
  const data = Object.entries(groupedByDate)
    .map(([date, prices]) => {
      return {
        date,
        ...prices,
      }
    })
    .sort((a, b) => {
      // Sort by date
      return new Date(a.date).getTime() - new Date(b.date).getTime()
    })

  // Get all supermarket names from the first data point
  const supermarkets = Object.keys(data[0]).filter((key) => key !== "date")

  // Generate a unique color for each supermarket
  const colors = [
    "#FF6384", // red
    "#36A2EB", // blue
    "#FFCE56", // yellow
    "#4BC0C0", // teal
    "#9966FF", // purple
    "#FF9F40", // orange
  ]

  return (
    <div className="w-full h-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" angle={-45} textAnchor="end" height={80} tick={{ fontSize: 12 }} />
          <YAxis />
          <Tooltip
            formatter={(value, name) => {
              // Extract supermarket ID from the name (e.g., "Supermarket 1" -> "1")
              const supermarketId = name.split(" ")[1]
              return [`$${value}`, `Supermarket ${supermarketId}`]
            }}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Legend />
          {supermarkets.map((supermarket, index) => (
            <Line
              key={supermarket}
              type="monotone"
              dataKey={supermarket}
              stroke={colors[index % colors.length]}
              activeDot={{ r: 8 }}
              name={supermarket}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
