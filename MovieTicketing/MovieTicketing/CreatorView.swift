//
//  CreatorView.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import SwiftUI

struct CreatorView: View {
    @State private var movie = Movie()
    @State private var password = ""
    @State private var theaternum = 4
    @EnvironmentObject var firestoreManager: FirestoreManager
    let validpassword = "movieadmin"
    var body: some View {
        VStack{
            Form{
                Section {
                    TextField("enter movie title", text: $movie.title)
                } header: {
                    Text("Title")
                }
                Section {
                    TextField("enter age rating", value: $movie.agerating, format: .number)
                } header: {
                    Text("Minimum Age Rating")
                }
                Section {
                    DatePicker("Select Showtime", selection: $movie.showdate).labelsHidden()
                } header: {
                    Text("Select Showtime")
                }
                Section {
                    Picker("Select Theater", selection: $movie.theater) {
                        ForEach(1..<11) {
                            Text("Theater \($0)")
                        }
                    }
                } header: {
                    Text("Select Showtime")
                }
                Section {
                    SecureField("enter creation password", text: $password)
                        .textContentType(/*@START_MENU_TOKEN@*/.password/*@END_MENU_TOKEN@*/)
                } header: {
                    Text("Admin Creation Password")
                }
            }
            Button {
                if (password == validpassword){
                    uploadNewMovie()
                } else {
                    print("password is incorrect")
                }
            } label: {
                Text("Create")
                    .padding()
                    .background(.blue)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
        
            }
            Spacer()
        }.navigationTitle("Create New Entry")
            .navigationBarTitleDisplayMode(.inline)
    }

    func uploadNewMovie(){
        firestoreManager.createMovie(movie)
    }
}

struct CreatorView_Previews: PreviewProvider {
    static var previews: some View {
        CreatorView().environmentObject(FirestoreManager())
    }
}
//    func connectToServer(){
//        if let client = try? Socket(.inet, type: .stream, protocol: .tcp) {
//            guard ((try? client.connect(port: 31337)) != nil) else {
//                return
//            }
//            let commandBytes = ([UInt8])("9ad97d87-8a70-4608-afb8-d7aae18cf84c::create::\(movie.title)::\(movie.agerating)::20222404::0630::01".utf8)
//            try? client.write(commandBytes)
//            let buffer_size = 8192
//            var buffer = [UInt8](repeating: 0, count: buffer_size) // allocate buffer
//            if let numberOfReadBytes = try? client.read(&buffer, size: buffer_size){
//                if (numberOfReadBytes > 0) {
//                    var command = String(bytes: buffer, encoding: .ascii)
//                    print(command)
//                }
//
//            }
//
//        }
//
//    }
