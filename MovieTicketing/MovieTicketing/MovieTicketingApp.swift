//
//  MovieTicketingApp.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import SwiftUI
import Firebase

@main
struct MovieTicketingApp: App {
    @StateObject var firestoreManager = FirestoreManager()
    init(){
        FirebaseApp.configure()
    }
    var body: some Scene {
        WindowGroup {
            ContentView().environmentObject(firestoreManager)
        }
    }
}
