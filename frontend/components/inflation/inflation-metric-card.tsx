import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { HelpCircle } from "lucide-react"

interface InflationMetricCardProps {
    title: string
    tooltipTitle: string
    tooltipDescription: string
    startValue: string
    endValue: string
    absoluteChange: string
    percentageChange: string
    startLabel?: string
    endLabel?: string
}

export function InflationMetricCard({
    title,
    tooltipTitle,
    tooltipDescription,
    startValue,
    endValue,
    absoluteChange,
    percentageChange,
    startLabel = "Start Basket Price:",
    endLabel = "End Basket Price:",
}: InflationMetricCardProps) {
    const percentageChangeNum = Number(percentageChange)
    const changeColorClass = percentageChangeNum === 0 ? "" : percentageChangeNum > 0 ? "text-red-500" : "text-green-500"

    return (
        <Card>
            <CardHeader className="pb-2">
                <div className="flex justify-between items-center">
                    <CardTitle className="text-lg">{title}</CardTitle>
                    <HoverCard>
                        <HoverCardTrigger>
                            <button type="button" className="rounded-full">
                                <HelpCircle className="h-4 w-4 text-gray-400" />
                            </button>
                        </HoverCardTrigger>
                        <HoverCardContent className="w-80">
                            <div className="space-y-2">
                                <h4 className="font-medium">{tooltipTitle}</h4>
                                <p className="text-sm text-gray-500">{tooltipDescription}</p>
                            </div>
                        </HoverCardContent>
                    </HoverCard>
                </div>
            </CardHeader>
            <CardContent>
                <div className="space-y-2">
                    <div className="flex justify-between">
                        <span className="text-sm text-gray-500">{startLabel}</span>
                        <span className="font-medium">${startValue}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-sm text-gray-500">{endLabel}</span>
                        <span className="font-medium">${endValue}</span>
                    </div>
                    <div className="flex justify-between pt-2 border-t">
                        <span className="text-sm text-gray-500">Absolute Change:</span>
                        <span className="font-medium">${absoluteChange}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-sm text-gray-500">Percentage Change:</span>
                        <span className={`font-medium ${changeColorClass}`}>{percentageChange}%</span>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

