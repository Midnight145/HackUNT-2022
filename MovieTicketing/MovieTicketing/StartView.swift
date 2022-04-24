//
//  ContentView.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import SwiftUI


struct ContentView: View {
    @State private var selection: String? = nil
    @EnvironmentObject var firestoreManager: FirestoreManager
    var body: some View {
        NavigationView {
            VStack {
                Spacer()
                NavigationLink(destination: CreatorView().environmentObject(firestoreManager), tag: "Create", selection: $selection) { EmptyView() }
                NavigationLink(destination: BookingView(movieTitles: firestoreManager.getMovies()).environmentObject(firestoreManager), tag: "Booking", selection: $selection) { EmptyView() }
                Button {
                    self.selection = "Booking"
                } label: {
                    Label("Get Tickets!", systemImage: "bag.circle")
                        .padding()
                        .frame(width: 200, height: 70, alignment: .center)
                        .background(Color.blue)
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                Spacer(minLength: 20)
                Button {
                    self.selection = "Create"
                } label: {
                    Label("Create Movie Entry", systemImage: "square.and.pencil")
                        .padding()
                        .frame(width: 250, height: 70, alignment: .center)
                        .background(Color.blue)
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                Spacer()
            }
            .navigationTitle("MOVIES++")
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView().environmentObject(FirestoreManager())
    }
}
