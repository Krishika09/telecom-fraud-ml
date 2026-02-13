"use client"

import { useEffect, useRef, useState } from "react"
import { motion } from "framer-motion"

// Simple Force Graph Simulation Mock
// In production optimize with D3 or Sigma.js

interface Node {
    id: number
    x: number
    y: number
    r: number
    color: string
}

interface Link {
    source: number
    target: number
}

export function NetworkGraph() {
    const [nodes, setNodes] = useState<Node[]>([])
    const [links, setLinks] = useState<Link[]>([])
    const containerRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        // Initialize random nodes
        const initialNodes: Node[] = []
        const initialLinks: Link[] = []

        // Create 3 clusters
        const clusters = [
            { cx: 30, cy: 30, color: "#ff4d4d", count: 15 }, // Red Cluster (High Risk)
            { cx: 70, cy: 70, color: "#ffca28", count: 10 }, // Yellow Cluster (Emerging)
            { cx: 70, cy: 30, color: "#64ffda", count: 8 },  // Green/Blue Cluster (Investigating)
        ]

        clusters.forEach((cluster, cIdx) => {
            const startIdx = initialNodes.length
            for (let i = 0; i < cluster.count; i++) {
                initialNodes.push({
                    id: startIdx + i,
                    x: cluster.cx + (Math.random() - 0.5) * 20,
                    y: cluster.cy + (Math.random() - 0.5) * 20,
                    r: Math.random() * 3 + 2,
                    color: cluster.color
                })

                // Link to previous node in cluster
                if (i > 0) {
                    initialLinks.push({
                        source: startIdx + i,
                        target: startIdx + Math.floor(Math.random() * i)
                    })
                }
            }
        })

        setNodes(initialNodes)
        setLinks(initialLinks)
    }, [])

    return (
        <div ref={containerRef} className="w-full h-[500px] border rounded-lg bg-black/40 relative overflow-hidden">
            <svg className="w-full h-full">
                {links.map((link, i) => {
                    const source = nodes[link.source]
                    const target = nodes[link.target]
                    if (!source || !target) return null
                    return (
                        <line
                            key={i}
                            x1={`${source.x}%`} y1={`${source.y}%`}
                            x2={`${target.x}%`} y2={`${target.y}%`}
                            stroke="rgba(255,255,255,0.1)"
                            strokeWidth="1"
                        />
                    )
                })}
                {nodes.map((node) => (
                    <motion.circle
                        key={node.id}
                        cx={`${node.x}%`}
                        cy={`${node.y}%`}
                        r={node.r}
                        fill={node.color}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1, x: [`${node.x}%`, `${node.x + (Math.random() - 0.5) * 2}%`, `${node.x}%`] }}
                        transition={{ duration: 2 + Math.random() * 2, repeat: Infinity }}
                        className="cursor-pointer hover:stroke-white hover:stroke-2"
                    />
                ))}
            </svg>
            <div className="absolute bottom-4 left-4 text-xs text-zinc-500">
                <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-500" /> Critical Cluster
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-yellow-400" /> Emerging Threat
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-teal-400" /> Investigating
                </div>
            </div>
        </div>
    )
}
