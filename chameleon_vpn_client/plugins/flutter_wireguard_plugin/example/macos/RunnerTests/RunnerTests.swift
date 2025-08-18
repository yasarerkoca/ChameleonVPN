import Cocoa
import FlutterMacOS
import XCTest


@testable import flutter_wireguard_plugin

// This demonstrates a simple unit test of the Swift portion of this plugin's implementation.
//
// See https://developer.apple.com/documentation/xctest for more information about using XCTest.

class RunnerTests: XCTestCase {

  func testGetPlatformVersion() {
    let plugin = FlutterWireguardPlugin()

    let call = FlutterMethodCall(methodName: "getPlatformVersion", arguments: [])

    let resultExpectation = expectation(description: "result block must be called.")
    plugin.handle(call) { result in
      XCTAssertEqual(result as! String,
                     "macOS " + ProcessInfo.processInfo.operatingSystemVersionString)
      resultExpectation.fulfill()
    }
    waitForExpectations(timeout: 1)
  }
  func testConnectDisconnect() {
    let plugin = FlutterWireguardPlugin()

    let connectCall = FlutterMethodCall(methodName: "connect", arguments: ["config": "[Interface]\nPrivateKey = x\nAddress = 10.0.0.2/32"])
    let connectExpectation = expectation(description: "connect result")
    plugin.handle(connectCall) { result in
      XCTAssertNotNil(result)
      connectExpectation.fulfill()
    }

    let disconnectCall = FlutterMethodCall(methodName: "disconnect", arguments: [])
    let disconnectExpectation = expectation(description: "disconnect result")
    plugin.handle(disconnectCall) { result in
      XCTAssertNotNil(result)
      disconnectExpectation.fulfill()
    }

    waitForExpectations(timeout: 1)
  }

}
