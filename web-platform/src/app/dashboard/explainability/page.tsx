"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

const featureImportance = [
    { name: "Call Duration < 3s", importance: 85, fill: "#ff4d4d" },
    { name: "High Frequency Outbound", importance: 78, fill: "#ffca28" },
    { name: "New Number Activation", importance: 65, fill: "#64ffda" },
    { name: "International Destination", importance: 45, fill: "#8884d8" },
    { name: "Non-Contact Ratio", importance: 40, fill: "#82ca9d" },
]

export default function ExplainabilityPage() {
    return (
        <div className="space-y-6">
            <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">AI Decision Explainability</h2>
                <p className="text-muted-foreground">Understanding why the grid flagged specific clusters as fraudulent.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Global Feature Importance (SHAP Values)</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={featureImportance} layout="vertical" margin={{ left: 40 }}>
                                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#333" />
                                    <XAxis type="number" stroke="#888" hide />
                                    <YAxis dataKey="name" type="category" stroke="#888" width={150} tick={{ fontSize: 12 }} />
                                    <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ backgroundColor: "#0a192f", border: "1px solid #333" }} />
                                    <Bar dataKey="importance" radius={[0, 4, 4, 0]} barSize={20} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Decision Logic: Wangiri Detection</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4 text-sm font-mono text-zinc-300">
                            <div className="p-3 border rounded bg-black/20">
                                <p className="text-primary mb-2">IF (Call_Duration &lt; 2s) AND (Callbacks_Received &gt; 50):</p>
                                <p className="pl-4 text-red-400">- RISK_SCORE += 40</p>
                                <p className="pl-4">- TAG = &quot;Wangiri Candidate&quot;</p>
                            </div>
                            <div className="p-3 border rounded bg-black/20">
                                <p className="text-primary mb-2">IF (Source_IP in Known_Botnet_Subnets):</p>
                                <p className="pl-4 text-red-400">- RISK_SCORE = 100</p>
                                <p className="pl-4">- ACTION = &quot;Immediate Block&quot;</p>
                            </div>
                            <div className="p-3 border rounded bg-black/20">
                                <p className="text-primary mb-2">IF (Behavior_Vector distance &lt; 0.05 from Cluster_492):</p>
                                <p className="pl-4 text-orange-400">- RISK_SCORE += 30</p>
                                <p className="pl-4">- TAG = &quot;Cluster Expansion&quot;</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
