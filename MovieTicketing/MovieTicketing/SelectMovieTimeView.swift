//
//  SelectMovieTimeView.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import SwiftUI

struct SelectMovieTimeView: View {
    @State var title: String
    @EnvironmentObject var firestoreManager: FirestoreManager
    @State private var movie = Movie()
    @State private var showdates = [Date]()
    @State private var showtimes = [String]()
    @State private var selectedDate = Date.now
    @State private var selectedTime = 0
    @State private var selectedMovie = Movie()
    var body: some View {
        VStack(spacing: 20){
            Text(title).font(.largeTitle)
            Text("Age Rating: \(movie.agerating)")
            DatePicker("", selection: $selectedDate, displayedComponents: .date)
                .labelsHidden()
                .onChange(of: selectedDate) { newValue in
                    print("new date is \(selectedDate.formatted(date: .long, time: .omitted))")
                }
            Picker("", selection: $selectedTime) {
//                ForEach(showdates, id: \.self) { showtime in
//                    Text(showtime.formatted(date: .omitted, time: .shortened))
//                }
                ForEach(showtimes, id: \.self) { showtime in
                    Text(showtime)
                }
            }.labelsHidden().pickerStyle(.wheel)
            NavigationLink {
                SelectSeatsView(id: showtimes[selectedTime]).environmentObject(firestoreManager)
            } label: {
                Text("Next")
                    .padding(.horizontal)
                    .padding(.vertical, 10)
                    .background(.blue)
                    .foregroundColor(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
            }
        }.onAppear {
            let dateString = selectedDate.formatted(date: .long, time: .omitted)
            showtimes = firestoreManager.getMovieTimes(fromTitle: title,  dateString: dateString)
        }.navigationTitle("Select Showtimes")
    }
    
    func getMoviee(fromTitle: String) {
        
        showdates = [Date(), Date().addingTimeInterval(6400), Date().addingTimeInterval(-6400)]
        movie = Movie()
    }
    
}

struct SelectMovieTimeView_Previews: PreviewProvider {
    static var previews: some View {
        SelectMovieTimeView(title: Movie().title)
    }
}
