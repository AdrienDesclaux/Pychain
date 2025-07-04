"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface WalletConnectProps {
  onConnect: (address: string) => void
  onDisconnect: () => void
  connectedAddress: string | null
}

export default function WalletConnect({ onConnect, onDisconnect, connectedAddress }: WalletConnectProps) {
  const [isConnecting, setIsConnecting] = useState(false)

  const connectWallet = async () => {
    if (typeof window.ethereum === "undefined") {
      alert("MetaMask is not installed. Please install MetaMask to continue.")
      return
    }

    setIsConnecting(true)
    try {
      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      })

      if (accounts.length > 0) {
        onConnect(accounts[0])
      }
    } catch (error) {
      console.error("Failed to connect wallet:", error)
      alert("Failed to connect wallet. Please try again.")
    } finally {
      setIsConnecting(false)
    }
  }

  const disconnectWallet = () => {
    onDisconnect()
  }

  useEffect(() => {
    // Check if already connected
    const checkConnection = async () => {
      if (typeof window.ethereum !== "undefined") {
        try {
          const accounts = await window.ethereum.request({
            method: "eth_accounts",
          })
          if (accounts.length > 0) {
            onConnect(accounts[0])
          }
        } catch (error) {
          console.error("Failed to check connection:", error)
        }
      }
    }

    checkConnection()

    // Listen for account changes
    if (typeof window.ethereum !== "undefined") {
      const handleAccountsChanged = (accounts: string[]) => {
        if (accounts.length > 0) {
          onConnect(accounts[0])
        } else {
          onDisconnect()
        }
      }

      window.ethereum.on("accountsChanged", handleAccountsChanged)

      return () => {
        window.ethereum.removeListener("accountsChanged", handleAccountsChanged)
      }
    }
  }, [onConnect, onDisconnect])

  if (connectedAddress) {
    return (
      <Card className="w-full max-w-md bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white">Wallet Connected</CardTitle>
          <CardDescription className="text-gray-400 break-all">{connectedAddress}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button
            onClick={disconnectWallet}
            variant="outline"
            className="w-full border-gray-600 text-gray-300 hover:bg-gray-700 bg-transparent"
          >
            Disconnect
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full max-w-md bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white">Connect MetaMask</CardTitle>
        <CardDescription className="text-gray-400">
          Connect your MetaMask wallet to access the blockchain explorer
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Button
          onClick={connectWallet}
          className="w-full bg-orange-600 hover:bg-orange-700 text-white"
          disabled={isConnecting}
        >
          {isConnecting ? "Connecting..." : "Connect MetaMask"}
        </Button>
      </CardContent>
    </Card>
  )
}
