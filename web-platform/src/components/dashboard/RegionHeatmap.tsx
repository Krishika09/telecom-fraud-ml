"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { motion } from "framer-motion"

const regions = [
    { name: "Maharashtra", threat: 85 },
    { name: "Delhi NCR", threat: 92 },
    { name: "Karnataka", threat: 45 },
    { name: "West Bengal", threat: 78 },
    { name: "Tamil Nadu", threat: 30 },
    { name: "Gujarat", threat: 60 },
    { name: "Uttar Pradesh", threat: 88 },
    { name: "Rajasthan", threat: 55 },
    { name: "Bihar", threat: 70 },
    { name: "Telangana", threat: 40 },
]

export function RegionHeatmap() {
    return (
        <Card className="col-span-4 lg:col-span-2">
            <CardHeader>
                <CardTitle>Regional Threat Heatmap</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-2 gap-4">
                    {regions.map((region) => (
                        <div key={region.name} className="flex items-center justify-between space-x-2">
                            <span className="text-sm font-medium">{region.name}</span>
                            <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden mx-2">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${region.threat}%` }}
                                    className={`h-full ${region.threat > 80 ? 'bg-red-500' : region.threat > 50 ? 'bg-orange-500' : 'bg-green-500'}`}
                                />
                            </div>
                            <span className="text-xs text-muted-foreground w-8 text-right">{region.threat}</span>
                        </div>
                    ))}
                </div>
                <div className="mt-4 text-xs text-center text-muted-foreground">
                    *Real-time aggregation from 14,203 towers
                </div>
            </CardContent>
        </Card>
    )
}
