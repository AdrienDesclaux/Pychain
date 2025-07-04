"use client"

import { useState } from "react"
import WalletConnect from "@/components/wallet-connect"
import BlockchainExplorer from "@/components/blockchain-explorer"

const AUTHORIZED_ADDRESS = "0x19a762e00dd1F5F0fcC308782b9ad2A7B127DF93"
const AUTHORIZED_ADDRESS2 = "0xc8911b67201e17b8506bb031dc8ecbc4c3d405c3"

export default function Home() {
  const [connectedAddress, setConnectedAddress] = useState<string | null>(null)

  const handleConnect = (address: string) => {
    setConnectedAddress(address)
  }

  const handleDisconnect = () => {
    setConnectedAddress(null)
  }

  if (!connectedAddress) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <WalletConnect onConnect={handleConnect} onDisconnect={handleDisconnect} connectedAddress={connectedAddress} />
      </div>
    )
  }

  if ((connectedAddress.toLowerCase() !== AUTHORIZED_ADDRESS.toLowerCase()) && (connectedAddress.toLowerCase() !== AUTHORIZED_ADDRESS2.toLowerCase())) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">ERROR</div>
          <h1 className="text-4xl font-bold text-red-500 mb-2">Access Denied</h1>
          <p className="text-gray-400">Your wallet address is not authorized to access this explorer.</p>
          <p className="text-sm text-gray-500 mt-2 break-all">Connected: {connectedAddress}</p>
          <div className="mt-4">
            <WalletConnect
              onConnect={handleConnect}
              onDisconnect={handleDisconnect}
              connectedAddress={connectedAddress}
            />
          </div>
        </div>
      </div>
    )
  }

  return <BlockchainExplorer />
}
