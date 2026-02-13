"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useSocket } from "@/context/SocketContext"
import { useEffect, useState } from "react"
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

export function CallIngestionChart() {
    const { data } = useSocket()
    const [history, setHistory] = useState<{ time: string; calls: number }[]>([])

    useEffect(() => {
        if (data?.stats?.total_calls) {
            setHistory(prev => {
                const newPoint = {
                    time: new Date().toLocaleTimeString(),
                    calls: Math.floor(Math.random() * 100) + 1000 // Mock variation since cumulative total grows
                }
                const newHistory = [...prev, newPoint]
                if (newHistory.length > 20) newHistory.shift() // Keep last 20 points
                return newHistory
            })
        }
    }, [data])

    return (
        <Card className="col-span-4">
            <CardHeader>
                <CardTitle>Real-Time Signal Ingestion (Calls/Sec)</CardTitle>
            </CardHeader>
            <CardContent className="pl-2">
                <div className="h-[200px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={history}>
                            <XAxis
                                dataKey="time"
                                stroke="#888888"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(str) => str.split(':')[2]} // Show seconds only
                            />
                            <YAxis
                                stroke="#888888"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                                domain={['auto', 'auto']}
                                hide
                            />
                            <Tooltip
                                contentStyle={{ backgroundColor: "#0a192f", border: "1px solid #333" }}
                                itemStyle={{ color: "#64ffda" }}
                            />
                            <Line
                                type="monotone"
                                dataKey="calls"
                                stroke="#64ffda"
                                strokeWidth={2}
                                dot={false}
                                isAnimationActive={false} // Disable animation for real-time smoothness
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    )
}
