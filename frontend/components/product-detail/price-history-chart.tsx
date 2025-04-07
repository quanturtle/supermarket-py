"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"

interface PriceHistoryChartProps {
  data: Array<{
    date: string
    [key: string]: string | number
  }>
}

export function PriceHistoryChart({ data }: PriceHistoryChartProps) {
  // Get all supermarket names from the first data point
  const supermarkets = Object.keys(data[0]).filter((key) => key !== "date")

  // Generate a unique color for each supermarket
  const colors = [
    "#FF6384", // red
    "#36A2EB", // blue
    "#FFCE56", // yellow
    "#4BC0C0", // teal
    "#9966FF", // purple
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
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip formatter={(value) => [`$${value}`, ""]} labelFormatter={(label) => `Date: ${label}`} />
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

