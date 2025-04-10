import { InflationResultCard } from "./inflation-result-card"
import { InflationGraph } from "./inflation-graph"
import type { ProductInflation } from "@/lib/api/api"

interface InflationResultsProps {
  results: {
    averagePriceInflation: {
      startPrice: string
      endPrice: string
      absoluteChange: string
      percentageChange: string
    }
    lowestPriceInflation: {
      startPrice: string
      endPrice: string
      absoluteChange: string
      percentageChange: string
    }
    priceGapInflation: {
      startGap: string
      endGap: string
      absoluteChange: string
      percentageChange: string
    }
    productInflation: ProductInflation[]
    startDate: string
    endDate: string
  }
}

export function InflationResults({ results }: InflationResultsProps) {
  return (
    <div className="mt-8 space-y-6">
      <h2 className="text-2xl font-bold">
        Inflation Results: {results.startDate} to {results.endDate}
      </h2>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Average Price Inflation */}
        <InflationResultCard
          title="Average Price Inflation"
          tooltipTitle="Average Price Inflation"
          tooltipDescription="This calculation takes the average price of each product across all supermarkets at both time points, then compares the total basket price to determine inflation. It represents the typical price change a consumer might experience."
          startValue={results.averagePriceInflation.startPrice}
          endValue={results.averagePriceInflation.endPrice}
          absoluteChange={results.averagePriceInflation.absoluteChange}
          percentageChange={results.averagePriceInflation.percentageChange}
        />

        {/* Lowest Price Inflation */}
        <InflationResultCard
          title="Lowest Price Inflation"
          tooltipTitle="Lowest Price Inflation"
          tooltipDescription="This calculation compares the lowest available price for each product at both time points. It represents the price change experienced by a consumer who always shops at the cheapest supermarket for each item."
          startValue={results.lowestPriceInflation.startPrice}
          endValue={results.lowestPriceInflation.endPrice}
          absoluteChange={results.lowestPriceInflation.absoluteChange}
          percentageChange={results.lowestPriceInflation.percentageChange}
          startLabel="Start Lowest Price:"
          endLabel="End Lowest Price:"
        />

        {/* Price Gap Inflation */}
        <InflationResultCard
          title="Price Gap Inflation"
          tooltipTitle="Price Gap Inflation"
          tooltipDescription="This measures how the difference between the highest and lowest prices (the 'gap') has changed over time. It calculates the percentage change in this gap for each product, then averages these changes. A positive value means price disparities are growing, while a negative value means prices are becoming more uniform."
          startValue={results.priceGapInflation.startGap}
          endValue={results.priceGapInflation.endGap}
          absoluteChange={results.priceGapInflation.absoluteChange}
          percentageChange={results.priceGapInflation.percentageChange}
          startLabel="Avg Start Gap:"
          endLabel="Avg End Gap:"
        />
      </div>

      {/* Per-Product Inflation Chart */}
      <InflationGraph data={results.productInflation} />
    </div>
  )
}
