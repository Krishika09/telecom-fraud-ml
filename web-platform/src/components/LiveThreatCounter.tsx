"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"

export function LiveThreatCounter() {
    const [count, setCount] = useState(1420310)
    const [activeThreats, setActiveThreats] = useState(0)

    useEffect(() => {
        const ws = new WebSocket("ws://127.0.0.1:8000/ws/threat-stream")

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            // data is { events: [...], stats: { total_calls, blocked_threats } }
            if (data.stats) {
                setCount(data.stats.total_calls)
                setActiveThreats(data.stats.blocked_threats)
            }
        }

        return () => {
            ws.close()
        }
    }, [])

    return (
        <div className="flex flex-col items-center justify-center p-6 bg-card/50 backdrop-blur border rounded-xl w-full max-w-md mx-auto mt-8">
            <h3 className="text-zinc-400 uppercase tracking-widest text-sm mb-2">Calls Processed (National)</h3>
            <motion.div
                key={count}
                initial={{ scale: 1.2, color: "#64ffda" }}
                animate={{ scale: 1, color: "#ffffff" }}
                className="text-5xl md:text-7xl font-mono font-bold text-white tabular-nums"
            >
                {count.toLocaleString()}
            </motion.div>

            <div className="mt-4 flex items-center gap-2 text-red-400">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                <span className="font-mono">{activeThreats} Threats Neutralized</span>
            </div>
        </div>
    )
}
