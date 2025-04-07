"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface DateSelectionCardProps {
    availableDates: string[]
    startDate: string
    endDate: string
    onStartDateChange: (date: string) => void
    onEndDateChange: (date: string) => void
    onCalculate: () => void
    isCalculateDisabled: boolean
}

export function DateSelectionCard({
    availableDates,
    startDate,
    endDate,
    onStartDateChange,
    onEndDateChange,
    onCalculate,
    isCalculateDisabled,
}: DateSelectionCardProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Select Time Period</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="start-date">Start Date</Label>
                        <Select value={startDate} onValueChange={onStartDateChange}>
                            <SelectTrigger id="start-date">
                                <SelectValue placeholder="Select start date" />
                            </SelectTrigger>
                            <SelectContent>
                                {availableDates.map((date) => (
                                    <SelectItem key={date} value={date}>
                                        {date}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="end-date">End Date</Label>
                        <Select value={endDate} onValueChange={onEndDateChange}>
                            <SelectTrigger id="end-date">
                                <SelectValue placeholder="Select end date" />
                            </SelectTrigger>
                            <SelectContent>
                                {availableDates.map((date) => (
                                    <SelectItem key={date} value={date}>
                                        {date}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </div>

                <Button onClick={onCalculate} className="w-full" disabled={isCalculateDisabled}>
                    Calculate Inflation
                </Button>

                {isCalculateDisabled && <p className="text-sm text-gray-500 text-center">Please select at least one product</p>}
            </CardContent>
        </Card>
    )
}

