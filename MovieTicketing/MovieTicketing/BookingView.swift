//
//  BookingView.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import SwiftUI

struct BookingView: View {
    @State private var selectedMovie = Movie()
    @EnvironmentObject var firestoreManager: FirestoreManager
    @State var movieTitles: [String]
    var body: some View {
        List(movieTitles, id: \.self) { movieTitle in
            NavigationLink {
                SelectMovieTimeView(title: movieTitle).environmentObject(firestoreManager)
            } label: {
                Text(movieTitle)
            }

        }.navigationTitle("Pick a title")
            .navigationBarTitleDisplayMode(.inline)
        
    }
}

//struct BookingView_Previews: PreviewProvider {
//    static var previews: some View {
//        BookingView()
//    }
//}
