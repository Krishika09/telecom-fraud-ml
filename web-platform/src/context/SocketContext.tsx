"use client"

import React, { createContext, useContext, useEffect, useState } from "react"

interface SocketContextType {
    data: any
    isConnected: boolean
}

const SocketContext = createContext<SocketContextType>({
    data: null,
    isConnected: false,
})

export const useSocket = () => useContext(SocketContext)

export function SocketProvider({ children }: { children: React.ReactNode }) {
    const [data, setData] = useState<any>(null)
    const [isConnected, setIsConnected] = useState(false)

    useEffect(() => {
        const ws = new WebSocket("ws://127.0.0.1:8000/ws/threat-stream")

        ws.onopen = () => setIsConnected(true)
        ws.onclose = () => setIsConnected(false)
        ws.onmessage = (event) => {
            try {
                const parsed = JSON.parse(event.data)
                setData(parsed)
            } catch (e) {
                console.error("Failed to parse WS message", e)
            }
        }

        return () => {
            ws.close()
        }
    }, [])

    return (
        <SocketContext.Provider value={{ data, isConnected }}>
            {children}
        </SocketContext.Provider>
    )
}
